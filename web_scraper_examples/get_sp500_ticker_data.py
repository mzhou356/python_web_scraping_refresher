import logging
from io import StringIO
from time import time
from datetime import datetime

import pandas as pd

from web_scraper_examples.scrape_sp500_tickers import get_sp500_symbols
from web_scraper_examples.scrape_yahoo_ticker_data import get_ticker_info

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)


START_TIME: time = time()


def get_all_ticker_data() -> pd.DataFrame:
    try:
        all_tickers = get_sp500_symbols()
    except Exception as exception:
        LOGGER.error("Failed to perform retrieve sp500 tickers due to this error %s",
                     exception)
        raise exception
    all_ticker_records = []
    for ticker in all_tickers:
        try:
            LOGGER.info("Getting data for ticker %s", ticker)
            ticker_record = get_ticker_info(ticker=ticker)
            ticker_record["time_collected"] = datetime.now()
        except Exception as exception:
            LOGGER.error("Failed to retrieve ticker information for this ticker % s due to error %s",
                         ticker, exception)
        else:
            all_ticker_records.append(ticker_record)
    return pd.DataFrame.from_records(data=all_ticker_records)


def save_to_csv(data: pd.DataFrame) -> str:
    string_buffer = StringIO()
    data.to_csv(string_buffer, index=False)
    return string_buffer.getvalue()


if __name__ == "__main__":
    print(save_to_csv(data=get_all_ticker_data()))
    print(f"This takes {time() - START_TIME} seconds")


