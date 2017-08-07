import requests


url = 'http://localhost:5000'
headers = {
    'Content-Type': 'application/json',
}


def get_client_services(client_id):
    handler = '/client/services'
    target_url = '{}{}'.format(url, handler)

    client_id = {
        "client_id": client_id
    }

    result = requests.post(target_url, json=client_id, headers=headers)

    return result.json()['items']


def get_all_available_services():
    handler = '/services'
    target_url = '{}{}'.format(url, handler)
    result = requests.get(target_url, headers=headers)
    return result.json()['items']


def get_client_available_services(client_id, balance):
    client_services = get_client_services(client_id)
    all_service = get_all_available_services()
    res = [service for service in all_service if service not in client_services]

    for service in res:
        if service['cost'] <= balance:
            return [service]

    return []

def add_service(client_id, service):
    handler = '/client/add_service'

    client_service = {
        "client_id": client_id,
        "service_id":   service['id']
    }

    target_url = '{}{}'.format(url, handler)

    result = requests.post(target_url, json=client_service, headers=headers)

    return result

