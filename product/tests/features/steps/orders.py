from behave import when, then
from selenium.webdriver.common.by import By


# 2 scenario
@when(u'Я перехожу во вкладку "{text}"')
def go_to_the_tab_orders(context, text):
    context.browser.find_element(By.LINK_TEXT, text).click()


@when(u'Я должен быть на странице списка новых заказов')
def should_be_at_new_orders_page(context):
    assert context.browser.current_url == \
           'http://127.0.0.1:8000/orders/%D0%9D%D0%BE%D0%B2%D1%8B%D0%B9/'


@when(u'Я нажимаю на кнопку "{text}" первой строки')
def push_button_detail_order(context, text):
    context.browser.find_element(By.LINK_TEXT, text).click()


@when(u'Я перехожу на детальный просмотр заказа')
def should_be_at_category_page(context):
    order_pk = context.browser.find_element(By.TAG_NAME, 'h5').text.split()[-1]
    assert context.browser.current_url == f'http://127.0.0.1:8000/order/{order_pk}'


@when(u'Я нажимаю на кнопку заказа "{text}"')
def push_button_accept_order(context, text):
    context.browser.find_element("name", text).click()


@then(u'Я должен быть на странице заказов в процессе')
def should_be_at_new_orders_page(context):
    assert context.browser.current_url == \
           'http://127.0.0.1:8000/orders/%D0%92%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%B5/'


# 3 scenario
@when(u'Я нажимаю на вкладку "{text}"')
def push_button_detail_order(context, text):
    context.browser.find_element(By.LINK_TEXT, text).click()


@when(u'Я должен быть на вкладке заказов в процессе')
def should_be_at_new_orders_page(context):
    assert context.browser.current_url == \
           'http://127.0.0.1:8000/orders/%D0%92%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%B5/'


@then(u'Я должен быть на странице завершенных заказов')
def should_be_at_new_orders_page(context):
    assert context.browser.current_url == \
           'http://127.0.0.1:8000/orders/%D0%92%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%BE/'
