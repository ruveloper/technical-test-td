from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from scraper.modules.wait import (
    wait_for_search_form_load,
    wait_for_load,
    wait_for_search_results,
)

URL = config("URL", cast=str)
TIMEOUT = config("TIMEOUT", cast=int)


def perform_search(driver, actor_type: str, actor_identifier: str) -> bool:
    """
    Performs a search on the website and return True if there are any legal process, otherwise return False.

    :param (WebDriver) driver: Selenium WebDriver.
    :param (str) actor_type:Actor type. Options: "actor", "defendant".
    :param (str) actor_identifier: Actor identification.
    :returns: (boolean) Search success.
    :raises ValueError: If an invalid search_by option is provided.
    """

    # Validate search_by parameter
    valid_search_options = ["actor", "defendant"]
    if actor_type.lower() not in valid_search_options:
        raise ValueError(f"Invalid actor_type option. Valid options are: {valid_search_options}")

    try:
        # * Go to the website
        driver.get(URL)

        # * Wait for the website to be loaded
        wait_for_load(driver)
        wait_for_search_form_load(driver)

        # * Get form elements
        form_container = driver.find_element(By.CLASS_NAME, "form-container")
        actor_input = form_container.find_element(By.CSS_SELECTOR, "input#mat-input-1")
        defendant_input = form_container.find_element(By.CSS_SELECTOR, "input#mat-input-3")
        submit_button = form_container.find_element(By.CSS_SELECTOR, "button[type='submit'].boton-buscar")

        # * Perform search
        if actor_type == "actor":
            actor_input.send_keys(actor_identifier)
        elif actor_type == "defendant":
            defendant_input.send_keys(actor_identifier)
        submit_button.click()
        print("SEARCH PERFORMED")

        # * Wait for the search results
        wait_for_load(driver)
        search_success = wait_for_search_results(driver)

        return search_success

    except Exception as e:
        raise Exception("TIMEOUT EXCEPTION | ", e)
