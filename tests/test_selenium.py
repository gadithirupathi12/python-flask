from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_app_loads():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=opts)

    driver.get("http://127.0.0.1:5000")

    assert "Employee" in driver.page_source  # adjust based on your page

    driver.quit()
