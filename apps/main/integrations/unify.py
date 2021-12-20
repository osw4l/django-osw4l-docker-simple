import time

from unificontrol import UnifiClient


class UnifyControllerIntegration(object):
    client: UnifiClient
    credentials = {}

    def __init__(self, **credentials):
        client = UnifiClient(host="35.171.47.213",
                             username='support@hotspote.com',
                             password='Rop34%dfT56',
                             port=8443,
                             site='ns8uch6b')
        self.credentials = credentials
        self.login(**credentials)

    def login(self, **credentials):
        self.client = UnifiClient(**credentials)
        return self.client

    def create_group(self, site_id, site_name):
        credentials = self.credentials.copy()
        credentials['site'] = site_id
        client = self.login(**credentials)
        group = client.create_usergroup(
            name=f'Default {site_name}',
            qos_rate_max_down=5,
            qos_rate_max_up=10
        )
        return group

    def create_site(self, name):
        site = self.client.create_site(name)[0]
        site_id = site.get("_id")
        try:
            group = self.create_group(
                site_id=site.get("name"),
                site_name=name
            )[0]
        except:
            self.delete_site(site_id)
            return None
        return {
            '_id': site_id,
            'name': site.get("name"),
            'group': group.get('_id')
        }

    def create_client(self, mac, name, user_group):
        site = self.client.create_site(name)[0]
        return {
            '_id': site.get("_id"),
            'name': site.get("name")
        }

    def delete_site(self, side_id):
        self.client.delete_site(side_id)

    def adopt_device(self, mac):
        self.client.adopt_device(mac)

    def get_sites(self):
        sites = self.client.list_sites()
        results = []
        for site in sites:
            results.append({
                'id': site.get('name'),
                'name': site.get('desc')
            })
        return results

    def create_hotspotop(self, name, password, note):
        return self.client.create_hotspotop(name, password, note)

    def get_hotspotop(self):
        return self.client.list_hotspotop()

