from django.core.management.base import BaseCommand
from unificontrol import UnifiClient
from apps.utils.colors import red, green, cyan
import json


class Command(BaseCommand):
    help = 'Create Super User Automatically'

    def handle(self, *args, **kwargs):
        print(green(msg='\nCollecting data ...'))
        client = UnifiClient(host="35.171.47.213",
                             username='support@hotspote.com',
                             password='Rop34%dfT56',
                             port=8443,
                             site='wb0wvx9e')

        print('guests')
        guests = client.list_guests()
        print(guests)

        print('clients')
        clients = client.list_clients()
        print(clients)

        print('sites')
        sites = client.list_sites()
        print(sites)

        print(green(json.dumps(sites)))

        for site in sites:
            print('{} - {}'.format(
                site.get('name'),
                site.get('desc')
            ))
            if 'dariel' in site.get('desc').lower():
                client.delete_site(site.get('_id'))

        r = client.create_hotspotop('sprt', '123', 'test')
        print(r)