import json
import concurrent.futures

from scraper import scraper

if __name__ == "__main__":
    """
    El siguiente caso de prueba tiene como objetivo verificar la capacidad de la solución de webscraping
    para ejecutar 15 consultas paralelas sin experimentar bloqueos.
    Se utilizan Threads para ejecutar 15 hilos de manera concurrente.
    """

    # * Define the search parameters
    search_parameters = [
        ("defendant", "1790598012001"),
        ("defendant", "1790337979001"),
        ("defendant", "0990340234001"),
        ("defendant", "1790283380001"),
        ("defendant", "0990049459001"),
        ("defendant", "0990379017001"),
        ("defendant", "0990017212001"),
        ("defendant", "0990023549001"),
        ("defendant", "1768037620001"),
        ("defendant", "1790016919001"),
        ("defendant", "0990347476001"),
        ("defendant", "0990026440001"),
        ("defendant", "1790319857001"),
        ("defendant", "0990011214001"),
        ("defendant", "0990001340001"),
    ]

    # * Execute the scraper
    data = []

    # * Define a function to scrape the data for a search parameter
    def scrape_data(search_parameter):
        actor_type, actor_identifier = search_parameter
        return scraper.scrape(actor_type, actor_identifier, headless=True, max_processes=5)

    # * Create a ThreadPoolExecutor with 15 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        # Submit the tasks to the executor
        futures = [executor.submit(scrape_data, search_parameter) for search_parameter in search_parameters]

        # Retrieve the results as they become available
        for future in concurrent.futures.as_completed(futures):
            data_from_results = future.result()
            data.append(data_from_results)

    # * Save the data to a JSON file
    with open("punto_1b_caso_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
