# cnio-api-py
This library passes requests to the changenow.io API located at https://changenow.io/api/v1 (version hardcoded for now)
Every API endpoint must be called using a PHP style http_build_query, and returns a JSON object
Currently the queries are built in each function to reduce dependencies, as they are essentially strings
appended to the end of the URL.
a query url to the api looks like this:
"https://changenow.io/api/v1/endpoint/param1/param2?<query_param_1>=<value>&<query_param_2>=<value>..."
Read the docs at https://changenow.io/api/docs for more information.

This module depends on requests, socketio and aiohttp.
