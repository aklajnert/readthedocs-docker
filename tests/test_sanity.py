import os
import time

from selenium.webdriver.common.by import By

DESIRED_RTD_VERSION = "5.8.2"
SHOW_BROWSER = os.environ.get("SHOW_BROWSER", False)


def test_sanity(app, sb):
    """Check if the basic functionality works correctly."""
    compose = app

    print("Starting selenium...")
    sb.get("http://localhost:{}".format(compose.open_port))

    version = sb.find_element(
        "#footer > div > div.footer-bottom > div.column-copyright > p:nth-child(2) > small > a"
    )
    assert version.text == DESIRED_RTD_VERSION

    _log_in(sb, compose.username, compose.password)

    assert sb.get_page_title() == "Project Dashboard | Read the Docs"

    # check if the documentation will be built properly
    time.sleep(1)
    sb.find_link_text("Import our own demo project").click()

    time.sleep(1)
    sb.find_link_text("Builds").click()

    while True:
        sb.refresh()
        builds = sb.find_elements("//li/div/a", by=By.XPATH)
        builds_text = [build.text.split(" ")[0] for build in builds]
        intermediate_states = ("Triggered", "Cloning", "Installing", "Building")
        if (
            builds_text[0] not in intermediate_states
            and builds_text[1] not in intermediate_states
        ):
            break
        else:
            time.sleep(1)

    assert builds_text == ["Passed", "Passed"], builds_text

    sb.find_link_text("View Docs").click()

    assert (
        sb.current_url
        == f"http://localhost:{compose.open_port}/docs/rtd-admin-demo/en/latest/"
    )
    assert (
        sb.find_element("h1", by=By.TAG_NAME).text
        == "Welcome to Read the Docs Template’s documentation!"
    )


def _log_in(driver, username, password):
    driver.find_link_text("Log in").click()
    driver.find_element("id_login", by=By.ID).send_keys(username)
    driver.find_element("id_password", by=By.ID).send_keys(password)
    driver.find_element("//button[contains(.,'Sign In')]", by=By.XPATH).click()
