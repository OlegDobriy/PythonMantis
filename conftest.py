from fixture.application import Application
import pytest
import json
import os.path
import ftputil
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
def app(request, config):
    global fixture
    browser = request.config.getoption('--browser')
    baseUrl = request.config.getoption('--baseUrl')
    web_config = config['web']
    webadmin_config = config['webadmin']  # открыть конфиг из json, часть с web
    if baseUrl is None:  # если задали URL в параметре запуска, то брать его, иначе брать из target.json
        baseUrl = web_config['baseUrl']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    fixture.session.check_login(username=webadmin_config['username'], password=webadmin_config['password'])
    return fixture

"""
@pytest.fixture(scope='session', autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])

    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)
"""

@pytest.fixture(scope='session')
def config(request):
    return load_config(request.config.getoption('--target'))


@pytest.fixture(scope='session', autouse=True)
def app_stop(request):
    def final():
        fixture.session.check_logout()
        fixture.destroy()
    request.addfinalizer(final)
    return fixture


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome')
    parser.addoption('--baseUrl', action='store')
    parser.addoption('--target', action='store', default='target.json')


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc.php.bak'):
            remote.remove('config_inc.php.bak')
        if remote.path.isfile('config_inc.php'):
            remote.rename('config_inc.php', 'config_inc.php.bak')
        remote.upload(os.path.join(os.path.dirname(__file__), 'resources/config_inc.php'), 'config_inc.php')


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc.php.bak'):
            if remote.path.isfile('config_inc.php'):
                remote.remove('config_inc.php')
                remote.rename('config_inc.php.bak', 'config_inc.php')
