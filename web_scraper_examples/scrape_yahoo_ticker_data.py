from typing import List, Dict

import requests
from bs4 import BeautifulSoup
import logging

BASE_URL: str = "https://finance.yahoo.com/quote/"

START_NAME: str = "Previous Close"

END_NAME: str = "1y Target Est"

LOGGER = logging.getLogger(__name__)


def _get_raw_data(ticker: str) -> List[str]:
    response = requests.get(BASE_URL+ticker, params={"p": ticker})
    parsed_soup = BeautifulSoup(response.text, "html.parser")
    all_stock_infos = parsed_soup.find_all(name="tr")
    return all_stock_infos


def get_ticker_info(ticker: str) -> Dict[str, str]:
    stock_infos = _get_raw_data(ticker=ticker)
    data = {"ticker": ticker}
    collect_flag = False
    for stock_info in stock_infos:
        infos = stock_info.find_all("td")
        try:
            name, value = infos
            if name.text == START_NAME:
                collect_flag = True
            if collect_flag:
                data[name.text] = value.text
            if name.text == END_NAME:
                break
        except Exception as exception:
            LOGGER.error("Failed to unpack this stock_info %s due to this exception %s",
                         stock_info,
                         exception)

    return data
