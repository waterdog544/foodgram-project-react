import pytest


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        email='testsuperuser@yandex.ru',
        username='TestSuperuser',
        first_name='Админ',
        last_name='Администратор',
        password='Qwerty123'
    )


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        email='testadmin@yandex.ru',
        username='TestAdmin',
        first_name='Админ',
        last_name='Администратор',
        password='Qwerty123'
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='vpupkin2@yandex.ru',
        username='vasya2.pupkin',
        first_name='Вася',
        last_name='Пупкин',
        password='Qwerty123'
    )


@pytest.fixture
def token_user_superuser(user_superuser):
    from rest_framework.authtoken.models import Token
    token = Token.for_user(user_superuser)

    return {
        'access': str(token.key),
    }


@pytest.fixture
def user_superuser_client(token_user_superuser):
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Token {token_user_superuser["access"]}'
    )
    return client


@pytest.fixture
def token_admin(admin):
    from rest_framework.authtoken.models import Token
    token = Token.for_user(admin)

    return {
        'access': str(token.key),
    }


@pytest.fixture
def admin_client(token_admin):
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Token {token_user_superuser["access"]}'
    )
    return client


@pytest.fixture
def token_user(user):
    from rest_framework.authtoken.models import Token
    token = Token.for_user(user)

    return {
        'access': str(token.key),
    }


@pytest.fixture
def user_client(token_user):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_user["access"]}')
    return client
