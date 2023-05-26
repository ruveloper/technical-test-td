import concurrent.futures
import json

from scraper import scraper

from decouple import config

PUNTO_1_MAX_PROCESS = config("PUNTO_1_MAX_PROCESS", cast=int, default=-1)

if __name__ == "__main__":
    """
    Ejecuta 4 consultas en la pagina web de Procesos Judiciales de Ecuador utilizando técnicas de Web Scraping
    almacenando los datos de resultados en un archivo JSON "punto_1_scraping_data.json".
    Se utilizan Threads para ejecutar un hilo de manera concurrente para cada parámetro de búsqueda.
    """

    # * Define the search parameters
    search_parameters = [
        ("actor", "0968599020001"),
        ("actor", "0992339411001"),
        ("defendant", "1791251237001"),
        ("defendant", "0968599020001"),
    ]

    # * Execute the scraper
    data = []

    # * Define a function to scrape the data for a search parameter
    def scrape_data(search_parameter):
        actor_type, actor_identifier = search_parameter
        return scraper.scrape(actor_type, actor_identifier, headless=True, max_processes=PUNTO_1_MAX_PROCESS)

    # * Create a ThreadPoolExecutor with 4 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit the tasks to the executor
        futures = [executor.submit(scrape_data, search_parameter) for search_parameter in search_parameters]

        # Retrieve the results as they become available
        for future in concurrent.futures.as_completed(futures):
            data_from_results = future.result()
            data.append(data_from_results)

    # * Save the data to a JSON file
    with open("punto_1_scraping_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
