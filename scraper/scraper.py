from decouple import config

from scraper.modules.data import get_data_from_search_results
from scraper.modules.driver import get_driver
from scraper.modules.search import perform_search

WEB_BROWSER = config("WEB_BROWSER", cast=str)


def scrape(actor_type, actor_identifier, headless=False, max_processes=-1) -> dict:
    """
    This function performs a search on the website of the Judicial Council of Ecuador and
    returns the data of the processes found using webscraping methods.

    :param (str) actor_type:Actor type. Options: "actor", "defendant".
    :param (str) actor_identifier: Actor identification.
    :param (bool) headless: If True, the browser will be executed in headless mode.
    :param (int) max_processes: Maximum number of processes to be scraped.
    :return: (dict) Data of the processes found.
    """
    try:
        # * Initialize a Selenium WebDriver
        driver = get_driver(WEB_BROWSER, headless)

        # * Perform a search
        success = perform_search(driver, actor_type, actor_identifier)

        # * Get the data from the search results
        if not success:
            return {
                "type": actor_type,
                "identifier": actor_identifier,
                "process_count": 0,
                "processes": [],
            }

        data_from_results: dict = get_data_from_search_results(driver, actor_type, actor_identifier, max_processes)

        # * Close the driver
        driver.quit()

        # * Return the data
        return data_from_results

    except Exception as e:
        raise Exception("SCRAPE EXCEPTION | ", e)
