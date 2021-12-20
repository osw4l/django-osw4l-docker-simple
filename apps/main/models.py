import uuid
from django.db import models
from django.template.defaultfilters import slugify
from colorfield.fields import ColorField
from apps.main.integrations.unify import UnifyControllerIntegration
from .constants import CONTROLLERS



class Controller(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    kind = models.CharField(
        max_length=50,
        choices=CONTROLLERS,
        unique=True
    )
    host = models.CharField(
        max_length=150,
        unique=True
    )
    port = models.PositiveIntegerField()
    username = models.CharField(
        max_length=50
    )
    password = models.CharField(
        max_length=50
    )

    class Meta:
        verbose_name = 'Controller'
        verbose_name_plural = 'Controllers'

    def __str__(self):
        return self.kind

    @property
    def credentials(self):
        return {
            'host': self.host,
            'username': self.username,
            'password': self.password,
            'port': self.port
        }


class PonemusCustomer(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=50
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    controller = models.ForeignKey(
        Controller,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Ponemus Customer'
        verbose_name_plural = 'Ponemus Customers'

    def __str__(self):
        return self.name


class Site(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    customer = models.ForeignKey(
        PonemusCustomer,
        on_delete=models.PROTECT
    )
    controller = models.ForeignKey(
        Controller,
        on_delete=models.PROTECT,
        editable=False,
        blank=True
    )
    slug = models.CharField(
        max_length=200,
        editable=False,
        blank=True,
        unique=True
    )
    site_name = models.CharField(
        max_length=200,
        unique=True
    )
    site_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )
    default_group_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    logo = models.ImageField(
        blank=True,
        null=True
    )
    container_color = ColorField(
        blank=True,
        null=True
    )
    background_color = ColorField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.controller = self.customer.controller
        self.slug = slugify(self.site_name)
        if not self.id:
            self.create_site()
        super().save(*args, **kwargs)

    def get_controller(self):
        controller = None
        if self.controller.kind == 'unify':
            controller = UnifyControllerIntegration(
                **self.controller.credentials
            )
        return controller

    def create_site(self):
        if self.controller.kind == 'unify':
            unify = UnifyControllerIntegration(
                **self.controller.credentials
            )
            site = unify.create_site(name=self.slug)
            if type(site) == dict:
                self.site_id = site.get('_id')
                self.site_name = site.get('name')
                self.default_group_id = site.get('group')

    def delete_site(self):
        if self.controller.kind == 'unify':
            try:
                unify = UnifyControllerIntegration(**self.controller.credentials)
                unify.delete_site(side_id=self.site_id)
            except:
                pass
            self.delete()


class CustomerSite(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE
    )
    mac_address = models.CharField(
        max_length=50
    )
    user_group_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=50
    )
    last_name = models.CharField(
        max_length=50
    )
    email = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    device = models.CharField(
        max_length=50
    )
    user_agent = models.CharField(
        max_length=50
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Customer Site'
        verbose_name_plural = 'Customer Sites'

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_controller_customer()
        super().save(*args, **kwargs)

    @property
    def name(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def create_controller_customer(self):
        if self.site.controller.kind == 'unify':
            credentials = self.site.controller.credentials.copy()
            credentials['site'] = self.site.site_id
            unify = UnifyControllerIntegration(
                **credentials
            )
            unify.create_client(
                name=self.get_full_name(),
                user_group=self.site.default_group_id,
                mac=self.mac_address
            )

