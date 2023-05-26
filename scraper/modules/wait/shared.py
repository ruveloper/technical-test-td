from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TIMEOUT = config("TIMEOUT", cast=int)


def wait_implicit_random(min_wait: int = 1, max_wait: int = 3) -> None:
    """
    Implicit wait for a random time between min_wait and max_wait.

    :param (int) min_wait: Minimum time to wait.
    :param (int) max_wait: Maximum time to wait.
    """
    import random
    import time

    time.sleep(random.randint(min_wait, max_wait))


def wait_for_load(driver, timeout=TIMEOUT) -> None:
    """
    Waits for the website, search or any request to be loaded.

    :param (WebDriver) driver: Selenium WebDriver.
    :param (int) timeout: Maximum time to wait for the website to be loaded.
    :raises TimeoutException: If the website is not loaded after the timeout.
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        wait.until(
            EC.all_of(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay")),
                EC.text_to_be_present_in_element_attribute(
                    (By.CSS_SELECTOR, "ng-progress div.ng-progress-bar"),
                    "active",
                    "false",
                ),
            )
        )
        wait_implicit_random()
    except Exception as e:
        raise Exception("WAIT_FOR_LOAD EXCEPTION: ", e)


def wait_for_element(driver, query_selector: str, timeout=TIMEOUT):
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, query_selector)))
        wait_implicit_random()
    except Exception as e:
        raise Exception("WAIT_FOR_ELEMENT EXCEPTION: ", e)
