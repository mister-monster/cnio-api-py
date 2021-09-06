DEPRACATED: changenow.io now maintains a python library that provides this functionality and is kept up to date with API changes. It can be found here https://gitlab.com/changenow-s-library-catalogue/changenow-api-python and it is recommended to use this library rather than mine.

This repository will no longer be maintained.

# cnio-api-py
This library passes requests to the changenow.io API located at https://changenow.io/api/v1 (version hardcoded for now)
Every API endpoint must be called using a PHP style http_build_query, and returns a JSON object
Currently the queries are built in each function to reduce dependencies, as they are essentially strings
appended to the end of the URL.
a query url to the api looks like this:
"https://changenow.io/api/v1/endpoint/param1/param2?<query_param_1>=<value>&<query_param_2>=<value>..."
Read the docs at https://changenow.io/api/docs for more information.

This module depends on requests, json and logging Python modules from the standard library.
