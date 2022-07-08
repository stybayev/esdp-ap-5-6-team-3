from django.urls import reverse


def get_resp_code(client, url):
    response = client.get(url)
    return response.status_code


def get_resp_status_code_from_url(client, url_name, user=None):
    if user:
        client.force_login(user)
    url = reverse(url_name)
    return get_resp_code(client, url)


def get_resp_code_url_with_arguments(client, url_name, model_object=None, user=None):
    if user:
        client.force_login(user)
    url = reverse(url_name, kwargs={'pk': model_object.pk})
    return get_resp_code(client, url)
