from behave import given, when, then
from selenium.webdriver.common.by import By


def find_category_pk(context):
    category_pk = context.browser.find_element(
        By.XPATH, "//input[@name='update_category']").get_attribute("value")
    return category_pk


# 1 scenario
@given(u'Я открыл страницу "Входа"')
def open_login_page(context):
    context.browser.get('http://127.0.0.1:8000/accounts/login/')


@when(u'Я ввожу текст "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element("name", f"{name}").send_keys(text)


@when(u'Я отправляю форму "{text}"')
def submit_form(context, text):
    context.browser.find_element("name", text).click()


@then(u'Я должен быть на главной странице')
def should_be_at_main(context):
    assert context.browser.current_url == 'http://127.0.0.1:8000/'


# 2 scenario
@given(u'Я нахожусь на главной странице')
def open_main_page(context):
    context.browser.get('http://127.0.0.1:8000/')


@when(u'Я нажимаю на кнопку "{text}"')
def click_button_category(context, text):
    context.browser.find_element("name", f"{text}").click()


@when(u'Я перехожу на страницу создания категории')
def should_be_at_create_category_page(context):
    assert context.browser.current_url == \
           'http://127.0.0.1:8000/category/add'


@then(u'Я должен видеть категорию "{text}" в списке')
def should_see_new_category(context, text):
    category_name = context.browser.find_element(By.LINK_TEXT, text)
    assert category_name.text == text


# 3 scenario
@when(u'Я нажимаю на кнпоку детального просмотра категории "{text}"')
def should_be_at_create_category_page(context, text):
    context.browser.find_element(By.LINK_TEXT, text).click()


@when(u'Я перехожу на страницу категории')
def should_be_at_category_page(context):
    assert \
        context.browser.current_url == \
        'http://127.0.0.1:8000/product/%D0%A7%D1%82%D0%BE-%D1%82%D0%BE/'


@when(u'Я нажимаю на кнопку изменения категории')
def click_button_update_category(context):
    category_pk = find_category_pk(context)
    context.browser.get(f'http://127.0.0.1:8000/category/{category_pk}/update')


@when(u'Я очищаю поле "{name}"')
def clear_field_category_for_update(context, name):
    context.browser.find_element("name", f"{name}").clear()


@when(u'Перехожу на страницу изменения категории')
def should_be_at_category_page(context):
    category_pk = find_category_pk(context)
    assert \
        context.browser.current_url == \
        f'http://127.0.0.1:8000/category/{category_pk}/update'


# 3 scenario
@when(u'Я перехожу на страницу категории "Что-то-2"')
def should_be_at_category_page(context):
    assert \
        context.browser.current_url == \
        'http://127.0.0.1:8000/product/%D0%A7%D1%82%D0%BE-%D1%82%D0%BE-2/'
