from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from scraper.modules.wait import wait_for_load


def go_to_page_by_link(driver, link_element: WebElement):
    """
    Go to the page by clicking on the link element.

    :param (WebDriver) driver: Selenium WebDriver.
    :param (WebElement) link_element: Link element.
    """
    try:
        link_element.click()
        wait_for_load(driver)
    except Exception as e:
        raise Exception("GO_TO_PAGE_BY_CLICK EXCEPTION: ", e)


def go_back_by_button(driver):
    """
    Go back by clicking on the button element return.

    :param (WebDriver) driver: Selenium WebDriver.
    """
    try:
        driver.find_element(By.CSS_SELECTOR, "button.btn-regresar").click()
        wait_for_load(driver)
    except Exception as e:
        raise Exception("GO_BACK_BY_BUTTON EXCEPTION: ", e)
