import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DESIRED_RTD_VERSION = "3.8.0"
SHOW_BROWSER = os.environ.get("SHOW_BROWSER", False)


class Driver:
    """Context manager to handle chrome driver."""

    def __init__(self):
        self.driver = None

    def __enter__(self):
        chrome_options = Options()
        if not SHOW_BROWSER:
            chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            Path(__file__).parent / "chromedriver_72.0.3626.7", options=chrome_options
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


def test_sanity(app):
    """Check if the basic functionality works correctly."""
    compose = app

    with Driver() as driver:
        print("Starting selenium...")
        driver.get("http://localhost:{}".format(compose.open_port))

        version = driver.find_element_by_xpath(
            "//a[@href='http://docs.readthedocs.io/page/changelog.html']"
        )
        assert version.text == DESIRED_RTD_VERSION

        _log_in(driver, compose.username, compose.password)

        assert driver.title == "Project Dashboard | Read the Docs"

        # check if the documentation will be built properly
        time.sleep(1)
        driver.find_element_by_link_text("Import our own demo project").click()

        time.sleep(1)
        driver.find_element_by_link_text("Builds").click()

        builds = driver.find_elements_by_xpath("//li/div/a")
        assert all(build.text.startswith("Passed") for build in builds)

        driver.find_element_by_link_text("View Docs").click()

        assert (
            driver.current_url
            == f"http://localhost:{compose.open_port}/docs/rtd-admin-demo/en/latest/"
        )
        assert (
            driver.find_element_by_tag_name("h1").text
            == "Welcome to Read the Docs Template’s documentation!"
        )


def _log_in(driver, username, password):
    driver.find_element_by_link_text("Log in").click()
    driver.find_element_by_id("id_login").send_keys(username)
    driver.find_element_by_id("id_password").send_keys(password)
    driver.find_element_by_xpath("//button[contains(.,'Sign In')]").click()
