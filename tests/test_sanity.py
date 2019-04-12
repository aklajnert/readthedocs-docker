import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DESIRED_RTD_VERSION = '3.4.1'


class Driver:
    """Context manager to handle chrome driver."""

    def __init__(self):
        self.driver = None

    def __enter__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(Path(__file__).parent / 'chromedriver', options=chrome_options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


def test_sanity(app):
    """Check if the basic functionality works correctly."""
    port, username, password = app

    with Driver() as driver:
        driver.get('http://localhost:{}'.format(port))

        version = driver.find_element_by_xpath("//a[@href='http://docs.readthedocs.io/page/changelog.html']")
        assert version.text == DESIRED_RTD_VERSION

        _log_in(driver, password, username)

        assert driver.title == 'Project Dashboard | Read the Docs'

        # check if the documentation will be built properly
        driver.find_element_by_link_text("Import our own demo project").click()
        driver.find_element_by_link_text("Builds").click()

        while True:
            builds = driver.find_elements_by_xpath("//li/div/a")
            if len(builds) == 1:
                builds[0].text.startswith("Triggered")
                time.sleep(10)
            else:
                break
        assert all(build.text.startswith("Passed") for build in builds)


def _log_in(driver, password, username):
    driver.find_element_by_link_text("Log in").click()
    driver.find_element_by_id('id_login').send_keys(username)
    driver.find_element_by_id('id_password').send_keys(password)
    driver.find_element_by_xpath("//button[contains(.,'Sign In')]").click()
