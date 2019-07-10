#! /usr/bin/python3

'''
This library passes requests to the changenow.io API located at https://changenow.io/api/v1 (version hardcoded for now)
Every API endpoint must be called using a PHP style http_build_query, and returns a JSON object
Currently the queries are built in each function to reduce dependencies, as they are essentially strings
appended to the end of the URL.
a query url to the api looks like this:
https://changenow.io/api/v1/<endpoint>/<param1>/<param2>?<query_param_1>=<value>&<query_param_2>=<value>...
Read the docs at https://changenow.io/api/docs for more information.
'''
import json
import requests
import logging

class cnio():
    def __init__(self):
        self.key = str()
        self.api = "https://changenow.io/api/v1/"

    def _get(self, url, headers=None, data=None, params=None):
        req = requests.get(url, headers=headers, data=data, params=params)
        if req.status_code not in [200, 201]:
            logging.error('get(%s) failed(%d)' % (url, req.status_code))
            if req.text is not None:
                logging.error('req: %s' % req.text)
                raise Exception('request.get() failed(%s)' % req.text)
            raise Exception(
                'request.get() failed(status_code:%d)' % req.status_code)
        return json.loads(req.text)

    def _post(self, url, headers=None, data=None):
        req = requests.post(url, headers=headers, data=data)
        if req.status_code not in [200, 201]:
            logging.error('post(%s) failed(%d)' % (url, req.status_code))
            if req.text is not None:
                raise Exception('request.post() failed(%s)' % req.text)
            raise Exception(
                'request.post() failed(status_code:%d)' % req.status_code)
        return json.loads(req.text)

    def get_pair(self):
        endpoint = str('/market-info/available-pairs/')
        endpoint = str(self.api + endpoint)
        return self._get(url=endpoint)

    def currencies(self, active, fixed_rate):
        # this method returns the list of supported currencies
        # Both params should be provided as a bool value
        query = str("?active=" + str(active) + "&fixedRate=" + str(fixed_rate))
        endpoint = "currencies"
        endpoint = str(self.api + endpoint + query)
        return self._get(url=endpoint)

    def currencies_to(self, ticker, fixed_rate):
        # this method returns a list of currencies that have trade pairs with the provided currency ticker
        # query param "fixed_rate" should be provided as a bool value
        query = str("?fixedRate=" + str(fixed_rate))
        endpoint = str("currencies-to/" + ticker)
        endpoint = str(self.api + endpoint + query)
        return self._get(url=endpoint)

    def specific_currency_info(self, ticker):
        # this method returns information on a specific currency
        endpoint = str("currencies/" + ticker)
        endpoint = str(self.api + endpoint)
        return self._get(url=endpoint)

    def min_amount(self, send, receive):
        # this method returns the minimum amount required to make an exchange.
        # you MUST provide the currency pair that you are looking to trade
        endpoint = str("min-amount/" + send + "_" + receive)
        endpoint = str(self.api + endpoint)
        return self._get(endpoint)

    def est_exchange_rate(self, send_amount, send, receive):
        # this method returns the amount of <recieve> currency you will get for the provided amount of <send> currency
        # you MUST provide the amount you intend to send, the currency to be sent and the currency to be recieved
        endpoint = str("exchange-amount/" + str(send_amount) + "/" + send + "_" + receive)
        endpoint = str(self.api + endpoint)
        return self._get(endpoint)

    def isitscam(self, url):
        # this endpoint just checks if the provided crypto site URL is valid or some type of scam
        # I am not sure how accurate the returned information will be
        endpoint = str("scam-check/" + url)
        endpoint = str(self.api + endpoint)
        return self._get(endpoint)

    # use this method to set an API key to work with for the duration of the instance
    # call it before calling any methods that require an API key
    def api_key(self, key):
        self.key = key

    # ALL OF THE FOLLOWING ENDPOINTS REQUIRE PROVISION OF AN API KEY
    # THE FOLLOWING ARE STANDARD FLOW (VARIABLE RATE NO LIMIT) API ENDPOINTS
    def create_transaction(self, send_amount, send, receive, addr, extra_id="", refund_address=""):
        # this endpoint creates a transaction
        # You must provide quite a bit of information. namely, send currency, recieve currency
        # the address you want the recieve currency sent to, the amount you will send,
        # and an "extra ID" for currencies that need it (eg. transaction ID for XMP)
        query = str("?from=" + send + "&to=" + receive + "&address=" + addr +
                         "&amount=" + str(send_amount) + "&extraId=" + extra_id + "&refundAddress=" + refund_address)
        endpoint = str("transactions/" + self.key)
        endpoint = str(self.api + endpoint + query)
        return self._post(endpoint)

    # THE FOLLOWING ARE THE FIXED RATE API ENDPOINTS
    def available_fixed_markets(self):
        # this method returns the available keypairs that can be exchanged at a fixed rate
        endpoint = str("market-info/fixed-rate/" + self.key)
        endpoint = str(self.api + endpoint)
        return self._get(endpoint)

    def estimate_fixed_rate_exchange_amount(self, send_amount, send, receive):
        # this method returns the amount of <recieve> currency you will get for the provided amount of <send> currency
        # you MUST provide the amount you intend to send, the currency to be sent and the currency to be recieved
        query = str("?api_key=" + self.key)
        endpoint = str("exchange-amount/fixed_rate/" + str(send_amount) + "/" + send + "_" + receive)
        endpoint = str(self.api + endpoint + query)
        return self._get(endpoint)

    def create_fixed_rate_transaction(self, send_amount, send, receive, addr, extra_id="", refund_address=""):
        # this endpoint creates a transaction
        # You must provide quite a bit of information. namely, send currency, recieve currency
        # the address you want the recieve currency sent to, the amount you will send,
        # and an "extra ID" for currencies that need it (eg. transaction ID for XMP)
        query = str("?from=" + send + "&to=" + receive + "&address=" + addr +
                    "&amount=" + str(send_amount) + "&extraId=" + extra_id + "&refundAddress=" + refund_address)
        endpoint = str("transactions/fixed_rate/" + self.key)
        endpoint = str(self.api + endpoint + query)
        return self._post(endpoint)

    # THE FOLLOWING CAN BE USED FOR VARIABLE AND FIXED RATE TRANSACTIONS
    def get_transaction_status(self, cnio_transaction_id):
        # this method returns the transaction status of a transaction. A transaction id
        # from list_transactions() or create_transaction() MUST be provided.
        endpoint = str("transactions/" + cnio_transaction_id + "/" + self.key)
        endpoint = str(self.api + endpoint)
        return self._get(endpoint)

    def list_transactions(self, send="", receive="", status="", limit="", offset=""):
        # this method returns a list of <limit> transactions that were started using the API key
        # All query parameters are optional, they are: sent currency, recieved currency, transaction status (for a
        # list of available statuses see the changenow API docs), limit (default 10) and offset, which is the
        # number of transactions to skip.
        # if none of these params are provided, the oldes 10 transactions will be returned, regardless
        # of status, currency, etc. No idea why they chose to show the oldest, but whatever.
        query = str("?from=" + send + "&to=" + receive + "&status=" + status + "&limit=" + limit + "&offset=" + offset)
        endpoint = str("transactions/" + self.key)
        endpoint = str(self.api + endpoint + query)
        return self._get(endpoint)


if __name__ != '__main__':
    cnio()
