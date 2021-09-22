import requests
import json
import logging
import sys
import logging.config


_STOCK_ANALYSIS_LOGFILE = "/var/log/stock_analysis.log"
_STOCK_ANALYSIS_TIMEOUT = 20

_MAX_LOG_FILE_SIZE = 10000000  # bytes
_MAX_LOG_FILES = 3
_LOG_LEVEL = logging.DEBUG


_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s | "
                      "%(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
        }
    },
    "handlers": {
        "default": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": _STOCK_ANALYSIS_LOGFILE,
            "mode": "a",
            "maxBytes": _MAX_LOG_FILE_SIZE,
            "backupCount": _MAX_LOG_FILES,
            "formatter": "default",
            "level": _LOG_LEVEL
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": _LOG_LEVEL
        },
        "root": {
            "handlers": ["default"],
            "level": _LOG_LEVEL
        }
    }
}

logging.config.dictConfig(_LOG_CONFIG)
logger = logging.getLogger("stock_anaylsis")

class HTTPConstants(object):
    _HTTP_OK = "200"
    _HTTP_NO_Content = "204"

url = "https://twelve-data1.p.rapidapi.com/quote"

querystring = {"symbol":"TCS:BSE","interval":"1day","outputsize":"30","format":"json"}

headers = {
    'x-rapidapi-host': "twelve-data1.p.rapidapi.com",
    'x-rapidapi-key': "1c632ed2ebmshfcfaca1bb6e07f1p188210jsn5e5003ff49b5"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


class StockAnalyst(object):
    def __init__(self, host, apikey):
        self.host = host
        self.api_key = apikey

    def get_quote(self, symbols, region="IN", interval="1min"):
        if not symbols:
            logger.error("Symbol is not there")
            return
        url = "https://" + self.host + "/market/v2/get-quotes"
        querystring = {"symbol":symbols,"region": region}
        headers = {
            'x-rapidapi-host': self.host,
            'x-rapidapi-key': self.api_key
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == HTTPConstants._HTTP_OK:
            print(response.content)


def main_func():
    stockObject = StockAnalyst("apidojo-yahoo-finance-v1.p.rapidapi.com",
                               "1c632ed2ebmshfcfaca1bb6e07f1p188210jsn5e5003ff49b5")
    stockObject.get_quote("TCS")


if __name__ == "__main__":
    sys.exit(main_func())
