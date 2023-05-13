import requests
from bs4 import BeautifulSoup

URL: str = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def get_sp500_symbols() -> str:
    response = requests.get(URL)
    parsed_html = BeautifulSoup(response.text, "html.parser")
    first_table = parsed_html.find("table")
    symbol_infos = first_table.find_all("a",  class_="external text")
    return tuple(symbol_info.text for symbol_info in symbol_infos)
