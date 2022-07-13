import pytest
from product.tests.test_helper import (
    get_resp_status_code_from_url, get_resp_code_url_with_arguments
)
from django.urls import reverse


@pytest.mark.django_db
def test_permission_main_page_by_unauthorized_user(client):
    assert get_resp_status_code_from_url(client, 'list_category') == 200


@pytest.mark.django_db
def test_permission_create_category_by_unauthorized_user(client):
    assert get_resp_status_code_from_url(client, 'create_category') == 302


@pytest.mark.django_db
def test_permission_create_category_by_authorized_user(client, user):
    assert get_resp_status_code_from_url(client, 'create_category',
                                         user) == 200


@pytest.mark.django_db
def test_permission_update_category_by_unauthorized_user(client, category):
    assert get_resp_code_url_with_arguments(client, 'update_category',
                                            category) == 302


@pytest.mark.django_db
def test_permission_update_category_by_authorized_user(client, category, user):
    assert get_resp_code_url_with_arguments(client, 'update_category',
                                            category, user) == 200


@pytest.mark.django_db
def test_permission_view_category_product_by_unauthorized_user(client,
                                                               product):
    url = reverse('list_category_product',
                  kwargs={'category': product.category})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_permission_create_product_by_unauthorized_user(client):
    assert get_resp_status_code_from_url(client, 'create_product') == 302


@pytest.mark.django_db
def test_permission_create_product_by_authorized_user(client, user):
    assert get_resp_status_code_from_url(client, 'create_product', user) == 200


@pytest.mark.django_db
def test_permission_update_product_by_unauthorized_user(client, product):
    assert get_resp_code_url_with_arguments(client, 'update_product',
                                            product) == 302


@pytest.mark.django_db
def test_permission_update_product_by_authorized_user(client, product, user):
    assert get_resp_code_url_with_arguments(client, 'update_product',
                                            product, user) == 200


@pytest.mark.django_db
def test_permission_view_detail_product_by_unauthorized_user(client, product):
    assert get_resp_code_url_with_arguments(client,
                                            'detail_product',
                                            product) == 200


@pytest.mark.django_db
def test_permission_view_feedbacks_by_unauthorized_user(client):
    assert get_resp_status_code_from_url(client, 'feedback_list') == 200


@pytest.mark.django_db
def test_permission_view_list_about_us_by_unauthorized_user(client):
    assert get_resp_status_code_from_url(client, 'aboutus_view') == 200


@pytest.mark.django_db
def test_permission_view_detail_about_us_by_unauthorized_user(client,
                                                              about_us):
    assert get_resp_code_url_with_arguments(client,
                                            'detail_aboutus',
                                            about_us) == 200


@pytest.mark.django_db
def test_permission_create_about_us_by_unauthorized_user(client):
    assert get_resp_status_code_from_url(client, 'create_aboutus') == 302


@pytest.mark.django_db
def test_permission_create_about_us_authorized_user(client, user):
    assert get_resp_status_code_from_url(client, 'create_aboutus', user) == 200


@pytest.mark.django_db
def test_permission_update_about_us_by_unauthorized_user(client, about_us):
    assert get_resp_code_url_with_arguments(client,
                                            'update_aboutus',
                                            about_us) == 302


@pytest.mark.django_db
def test_permission_update_about_us_by_authorized_user(client, about_us, user):
    assert get_resp_code_url_with_arguments(client,
                                            'update_aboutus',
                                            about_us,
                                            user) == 200


@pytest.mark.django_db
def test_permission_view_order_list_by_unauthorized_user(client, order_status):
    url = reverse('orders_view', kwargs={'status': order_status.status})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_permission_view_order_list_by_authorized_user(client,
                                                       user,
                                                       order_status):
    client.force_login(user)
    url = reverse('orders_view', kwargs={'status': order_status.status})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_permission_view_detail_order_by_authorized_user(client, user, order):
    assert get_resp_code_url_with_arguments(client, 'detail_order',
                                            order, user) == 200
