import cnio_api
import json
import time

cnio = cnio_api.cnio()

# test parameters
key = "baa822014e8c99942f6afbacbc52ec23b43ffabc768f33a2ad2e65d24675355d"
recieve_address = "0x5736db83d42a64C278ECe5D61C8bA8A821A76785"
extra_id = None

# set the API key for the cnio_api instance for all methods that need it
cnio.api_key(key)

# every # is a test of another endpoint. There are 8 endpoints total, only 7 are tested here (socketsio incomplete)
# create_transaction() is commented out because we don't want to spam changenow with transactions
# however, it must be run at least once to test list_transactions() and get_transaction_status()
# add optional query params to the method calls to test those
# this is to test the python library, not to test the changenow API, so we aren't going to run the test with
# a million pairs or every possible optional parameter. That is outside of the scope of this test

#
print(cnio.min_amount("BTC", "ETH"))
print("===")
#
print(cnio.currencies(active=True))
print("===")
#
print(cnio.est_exchange_rate("1","BTC","ETH"))
print("===")
#
print(cnio.isitscam("changenow.io"))
print("===")

#
#print(cnio.create_transaction("1","BTC","ETH",recieve_address))
#print("===")

#
transactions_list = cnio.list_transactions(limit="2")
print(transactions_list)

print("===")
transactions_list = str(transactions_list).replace("b'[","")
transactions_list = transactions_list.replace("]'","")
transactions_list = transactions_list.replace("},{","} , {")
transactions_list = transactions_list.split(" , ")
for i in transactions_list:
    i = json.loads(i)
    #
    print(cnio.get_transaction_status(i["id"]))
    time.sleep(1)