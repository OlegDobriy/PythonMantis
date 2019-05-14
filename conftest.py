from fixture.application import Application
import pytest
import json
import os.path
import importlib
import jsonpickle

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        path_to_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(path_to_config_file) as config_file:
            target = json.load(config_file)
    return target


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption('--browser')
    baseUrl = request.config.getoption('--baseUrl')
    web_config = load_config(request.config.getoption('--target'))['web']
    webadmin_config = load_config(request.config.getoption('--target'))['webadmin']# открыть конфиг из json, часть с web
    if baseUrl is None:  # если задали URL в параметре запуска, то брать его, иначе брать из target.json
        baseUrl = web_config['baseUrl']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=baseUrl)
    fixture.session.check_login(username=webadmin_config['username'], password=webadmin_config['password'])
    return fixture


@pytest.fixture(scope='session', autouse=True)
def app_stop(request):
    def final():
        fixture.session.check_logout()
        fixture.destroy()
    request.addfinalizer(final)
    return fixture


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--baseUrl', action='store')
    parser.addoption('--target', action='store', default='target.json')
