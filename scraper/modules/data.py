import re

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from scraper.modules.utils import go_to_page_by_link, go_back_by_button
from scraper.modules.wait import wait_for_load, wait_for_element


def get_data_from_search_results(
    driver: WebDriver, actor_type: str, actor_identifier: str, max_processes: int = -1
) -> dict:
    """
    Get the data from the search results.

    :param (WebDriver) driver: Selenium WebDriver.
    :param (str) actor_type:Actor type. Options: "actor", "defendant".
    :param (str) actor_identifier: Actor identification.
    :param (int) max_processes: Maximum number of processes to be scraped.
    :returns: (dict) Search results.
    """
    try:
        # * Get the count of results
        data_from_results: dict = {
            "type": actor_type,
            "identifier": actor_identifier,
            "process_count": 0,
            "processes": [],
        }

        # * Get the count of process
        # try 3 times if the count is not found
        process_count = 0
        for i in range(3):
            text_count = driver.find_element(
                By.CSS_SELECTOR, "section.registros-encontrados > p.cantidadMovimiento"
            ).text
            extract_count = re.search(r"(\d+)", text_count)
            process_count = int(extract_count.group(1))
            if process_count > 0:
                break
            if i == 2:
                raise Exception("GET_DATA_FROM_SEARCH_RESULTS EXCEPTION: Count not found")
            # Refresh the page
            driver.refresh()
            wait_for_load(driver)
        data_from_results["process_count"] = process_count

        # * Limit the number of processes to be scraped if max_processes is set to a positive value
        if max_processes > 0:
            process_count = min(process_count, max_processes)
            data_from_results["process_count"] = process_count

        # * Get the process data for each page
        # Get the number of pages
        pages_count = process_count // 10 + 1
        for process_id in range(1, process_count + 1):
            # Refresh the page to ensure that the page content fully loaded
            driver.refresh()
            wait_for_load(driver)

            # * Go to the process page
            process_page_number = process_id // 10 + 1
            if process_page_number > 1:
                for i in range(2, process_page_number + 1):
                    try:
                        page_next_button = driver.find_element(
                            By.CSS_SELECTOR, "button.mat-mdc-paginator-navigation-next"
                        )
                        page_next_button.click()
                        wait_for_load(driver)
                    except Exception as e:
                        raise Exception(
                            "GET_DATA_FROM_SEARCH_RESULTS EXCEPTION: Go to process page | ",
                            e,
                        )

            # * GET THE PROCESS GENERAL DATA
            # * ----------------------------------------
            process_data = {}

            # Get process entry element from the list based on the process id
            process_entries = driver.find_elements(By.CSS_SELECTOR, "div.cuerpo > div.causa-individual")
            process_entry = None
            for entry in process_entries:
                if process_id == int(entry.find_element(By.CSS_SELECTOR, "div.id").text):
                    process_entry = entry
                    break
            if not process_entry:
                continue

            # Get the data from the process entry
            process_data["id"] = process_entry.find_element(By.CSS_SELECTOR, "div.id").text
            process_data["date"] = process_entry.find_element(By.CSS_SELECTOR, "div.fecha").text
            process_data["process_number"] = process_entry.find_element(By.CSS_SELECTOR, "div.numero-proceso").text
            process_data["infringement"] = process_entry.find_element(By.CSS_SELECTOR, "div.accion-infraccion").text

            # * GET THE PROCESS DETAILS
            # * ----------------------------------------
            process_data["process_details"] = []

            # Go to the process details page
            link_element = process_entry.find_element(By.CSS_SELECTOR, "div.detalle > a")
            go_to_page_by_link(driver, link_element)

            # Count all the process details entries
            process_details_entries_query_selector = (
                "div.lista-movimientos-causa > div.cuerpo > div.movimiento-individual"
            )
            process_details_entries_count = len(
                driver.find_elements(By.CSS_SELECTOR, process_details_entries_query_selector)
            )
            # Get the data from the process details entries
            for i in range(process_details_entries_count):
                # Get the process details entry element on each iteration since the page is refreshed
                process_details_entries = driver.find_elements(By.CSS_SELECTOR, process_details_entries_query_selector)
                process_details_entry = process_details_entries[i]

                # Get the data from the process details entry
                process_detail = {}
                process_detail["dependency"] = process_details_entry.find_element(
                    By.CSS_SELECTOR, "div.detalle-movimiento > span"
                ).text[28:]
                process_detail["city"] = process_details_entry.find_element(
                    By.CSS_SELECTOR, "div.detalle-movimiento > div"
                ).text[8:]
                process_detail["number"] = process_details_entry.find_element(
                    By.CSS_SELECTOR,
                    "div.lista-movimiento-individual > div.numero-incidente",
                ).text
                process_detail["date"] = process_details_entry.find_element(
                    By.CSS_SELECTOR,
                    "div.lista-movimiento-individual > div.fecha-ingreso",
                ).text
                process_detail["actors"] = process_details_entry.find_element(
                    By.CSS_SELECTOR,
                    "div.lista-movimiento-individual > div.lista-actores",
                ).text
                process_detail["defendants"] = process_details_entry.find_element(
                    By.CSS_SELECTOR,
                    "div.lista-movimiento-individual > div.lista-demandados",
                ).text

                # * GET THE PROCEEDINGS DETAILS
                # * ----------------------------------------
                process_detail["proceedings"] = []

                # go to the procedings details page
                link_element = process_details_entry.find_element(
                    By.CSS_SELECTOR,
                    "div.lista-movimiento-individual > div.actuaciones-judiciales > a",
                )
                go_to_page_by_link(driver, link_element)

                # Expand all proceedings
                wait_for_load(driver)
                wait_for_element(driver, "div.panel-expansion-action-buttons > button:first-child")
                expand_all_button = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.panel-expansion-action-buttons > button:first-child",
                )
                expand_all_button.click()

                # Get the proceedings entries
                # since the data is in the same page, we can use the same references in the loop
                proceeding_entries = driver.find_elements(
                    By.CSS_SELECTOR,
                    "mat-accordion > mat-expansion-panel.mat-expansion-panel",
                )
                for proceeding_entry in proceeding_entries:
                    proceedings_detail = {}
                    # Get date and title
                    proceeding_headers = proceeding_entry.find_elements(By.CSS_SELECTOR, "div.cabecera-tabla > span")
                    proceedings_detail["date"] = proceeding_headers[0].text
                    proceedings_detail["title"] = proceeding_headers[1].text
                    # Get the proceeding content
                    proceeding_content = proceeding_entry.find_element(
                        By.CSS_SELECTOR,
                        "div.mat-expansion-panel-content article.actividad",
                    ).text
                    proceedings_detail["content"] = proceeding_content

                    # Add the proceeding detail to proceedings
                    process_detail["proceedings"].append(proceedings_detail)

                # ! Return to the process details page
                go_back_by_button(driver)
                # * ----------------------------------------

                # Add the process detail to the process data
                process_data["process_details"].append(process_detail)

            # ! Return to the search results page
            go_back_by_button(driver)
            # * ----------------------------------------

            # Add the process data to the results
            data_from_results["processes"].append(process_data)
            print(f"PROCESS {process_id} OF {process_count}")

        return data_from_results

    except Exception as e:
        raise Exception("GET_DATA_FROM_SEARCH_RESULTS EXCEPTION | ", e)
