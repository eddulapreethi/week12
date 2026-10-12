import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    yield driver
    driver.quit()

def get_alert_text(driver):
    alert=Alert(driver)
    text=alert.text
    alert.accept()
    return text

def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.ID, "name").clear()
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Name cannot be empty"

def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.ID, "name").send_keys("Preethi")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "submit").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty"

def test_valid_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.ID, "name").send_keys("Preethi")
    driver.find_element(By.ID, "password").send_keys("p123")
    driver.find_element(By.ID, "submit").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 characters long"

def test_successful_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.ID, "name").send_keys("Preethi")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()
    time.sleep(2)
    current_url=driver.current_url
    assert "/submit" in current_url, f"Expected redirect to successful.html, but get: {current_url}"
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Registration Successful Preethi" in body_text, f"Greeting not found or incorrect: {body_text}"