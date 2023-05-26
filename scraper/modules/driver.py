from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def get_driver(browser: str, headless: bool = False) -> webdriver:
    """
    Get a Selenium WebDriver for the specified browser

    :param browser: The browser to use
    :param headless: If the browser should be headless
    :return: A Selenium WebDriver
    """
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
    elif browser == "chromium":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            options=options,
        )
        return driver
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        return driver
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        return driver
    else:
        raise Exception("Browser not supported for scraping")
