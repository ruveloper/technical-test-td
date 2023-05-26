from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TIMEOUT = config("TIMEOUT", cast=int)


def wait_for_search_form_load(driver, timeout=TIMEOUT) -> None:
    """
    Waits for the search form to be loaded.

    :param (WebDriver) driver: Selenium WebDriver.
    :param (int) timeout: Maximum time to wait for the website to be loaded.
    :raises TimeoutException: If the search form is not loaded after the timeout.
    """
    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.all_of(
                EC.visibility_of_element_located((By.CLASS_NAME, "form-container")),
                EC.visibility_of_element_located((By.CSS_SELECTOR, "form.form-container input#mat-input-1")),
                EC.visibility_of_element_located((By.CSS_SELECTOR, "form.form-container input#mat-input-3")),
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "form.form-container button[type='submit'].boton-buscar",
                    )
                ),
                EC.visibility_of_element_located((By.CSS_SELECTOR, "form.form-container div.grecaptcha-badge")),
            )
        )
    except Exception as e:
        raise Exception("WAIT_FOR_FORM EXCEPTION: ", e)


def wait_for_search_results(driver, timeout=TIMEOUT) -> bool:
    """
    Waits for the results of the search, if there are data as results, return True.

    :param (WebDriver) driver: Selenium WebDriver.
    :param (int) timeout: Maximum time to wait for the website to be loaded.
    :returns: (bool) True if there are data as results, False otherwise.
    :raises TimeoutException: If the search data is not loaded after the timeout.
    """
    try:
        # Wait for any element which indicates that the search is done
        # and obtain the element that triggered the wait
        element: WebElement = WebDriverWait(driver, TIMEOUT).until(
            EC.any_of(
                # Check if snackbar of any kind is visible
                EC.visibility_of_element_located((By.CSS_SELECTOR, "simple-snack-bar")),
                # Check if there are results
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "section.causas > div.cuerpo > div.causa-individual",
                    )
                ),
            )
        )

        # If the element is the snackbar with a specific text, then there are no results
        if element.tag_name == "simple-snack-bar" and "no devolvió resultados" in element.text:
            # Close the snackbar
            close_button: WebElement = element.find_element(By.CSS_SELECTOR, "button[matsnackbaraction]")
            close_button.click()
            print("NO RESULTS FOUND")
            return False
        # If the element is an individual result, then there are results
        elif element.tag_name == "div" and "causa-individual" in element.get_attribute("class"):
            print("RESULTS FOUND")
            return True
        # If the element is something else, then there was an error
        else:
            raise Exception("WAIT_FOR_SEARCH_RESULTS EXCEPTION: element is not recognized")

    except Exception as e:
        raise Exception("WAIT_FOR_SEARCH_RESULTS EXCEPTION: ", e)
