from behave import fixture, use_fixture
from selenium import webdriver


@fixture
def browser_chrome(context):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(30)
    context.browser = driver
    yield context.browser
    context.browser.quit()


def before_all(context):
    use_fixture(browser_chrome, context)
