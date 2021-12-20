from unificontrol import UnifiClient
from tabulate import tabulate

def run():
    client = UnifiClient(host="35.171.47.213",
                         username='support@hotspote.com',
                         password='Rop34%dfT56',
                         port=8443,
                         site='ns8uch6b')

    guests = client.list_guests(within=5000)
    print(guests)

    print('clients')
    clients = client.list_clients()
    print(clients)

