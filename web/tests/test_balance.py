import pytest
import time

from client_services import add_service
from client_services import get_client_services, get_all_available_services, get_client_available_services
from db_adapter import get_balance, get_clients_with_balance_positive
from db_adapter import create_new_client_with_balance


@pytest.fixture(scope='class')
def client_and_service():

    clients_with_balance_positive = get_clients_with_balance_positive()
    all_services = get_all_available_services()

    for client in clients_with_balance_positive:
        client_id = client[0]
        balance = get_balance(client_id)
        client_available_services = get_client_available_services(client[0], balance)
        if len(client_available_services) != 0:
            return client_id, client_available_services[0], get_balance(client_id)

    new_client_name = 'Ivan Petrovich'
    client_id = create_new_client_with_balance(new_client_name, 5.0)

    return client_id, all_services[0], get_balance(client_id)


@pytest.mark.usefixtures('client_and_service')
class Test:

    def test_add_service_response_code(self, client_and_service):
        client_id = client_and_service[0]
        service = client_and_service[1]

        print get_client_services(client_id)
        assert add_service(client_id, service).status_code == 202

    def test_new_service_availdble_after_1_minute(self, client_and_service):
        client_id = client_and_service[0]
        service = client_and_service[1]

        timer = 0
        while timer < 60:
            services = get_client_services(client_id)
            if service in services:
                break
            timer += 1
            time.sleep(1)

        assert timer != 60

    def test_change_balance_when_add_new_service(self, client_and_service):
        client_id = client_and_service[0]
        service = client_and_service[1]
        client_balance_before = client_and_service[2]

        balance_after = get_balance(client_id)
        assert client_balance_before - service['cost'] == balance_after

