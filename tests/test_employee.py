import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL

class TestEmployeeDirectory:

    def test_page_loads(self, driver):
        """Test that the application loads successfully via VM IP."""
        driver.get(BASE_URL)
        assert 'Employee Directory' in driver.title
        assert driver.find_element(By.ID, 'addBtn').is_displayed()

    def test_add_employee_appears_in_list(self, driver):
        """Test adding an employee and verifying it appears in the list."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)

        # Enter employee name
        name_input = wait.until(EC.presence_of_element_located((By.ID, 'empName')))
        name_input.clear()
        name_input.send_keys('Alice Johnson')

        # Click Add Employee button
        add_btn = driver.find_element(By.ID, 'addBtn')
        add_btn.click()

        # Wait for list to update and verify employee appears
        wait.until(EC.text_to_be_present_in_element((By.ID, 'empList'), 'Alice Johnson'))
        emp_list = driver.find_element(By.ID, 'empList').text
        assert 'Alice Johnson' in emp_list, f'Employee not found in list: {emp_list}'

    def test_multiple_employees(self, driver):
        """Test adding multiple employees."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        employees = ['Bob Smith', 'Carol White']

        for emp in employees:
            inp = wait.until(EC.presence_of_element_located((By.ID, 'empName')))
            inp.clear()
            inp.send_keys(emp)
            driver.find_element(By.ID, 'addBtn').click()
            import time; time.sleep(0.5)

        emp_list_text = driver.find_element(By.ID, 'empList').text
        for emp in employees:
            assert emp in emp_list_text
