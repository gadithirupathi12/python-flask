import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

VM_IP   = '43.205.142.37'   # Replace with your actual VM IP
VM_PORT = '5000'
from tests.conftest import BASE_URL   ✅

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()
