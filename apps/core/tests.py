import pytest
from django.test import Client

@pytest.mark.django_db
def test_example():
    assert 1 == 1

def test_index_view(client: Client):
    response = client.get("/")
    assert response.status_code == 404


