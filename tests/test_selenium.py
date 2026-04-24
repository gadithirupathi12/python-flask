import pytest, os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get("APP_URL", "http://127.0.0.1:5000")

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=opts)
    yield d
    d.quit()

def test_add_employee(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    name_input = wait.until(EC.presence_of_element_located((By.ID, "empName")))
    name_input.clear()
    name_input.send_keys("Alice Johnson")

    add_btn = driver.find_element(By.ID, "addBtn")
    add_btn.click()

    time.sleep(1)

    emp_list = wait.until(EC.presence_of_element_located((By.ID, "empList")))
    items = emp_list.find_elements(By.TAG_NAME, "li")
    names = [li.text for li in items]

    assert "Alice Johnson" in names, f"Expected 'Alice Johnson' in list, got: {names}"
