from getpass import getpass
from urllib.error import HTTPError

from sedas_pyapi.sedas_api import SeDASAPI


if __name__ == '__main__':

    # creating the SeDASAPI object attempts to log into live. It will throw an exception if it cant. so we feed it real creds (any one using test should have a live set)
    _username = input("Please enter your live username:")
    __password = getpass("Please enter your live password:")

    # Note the SeDASBulkDownload is very chatty at debug. But if you need to know what is going on enable logging.
    logging.basicConfig(level=logging.DEBUG)
    _logger.setLevel(logging.DEBUG)

    # create the object this will connect to the test.
    sedas = SeDASAPI(_username, __password)

    # set the base url to point at the test instance
    sedas.base_url = "https://geobrowsertest.satapps.org/api/"

    # Now we need to reset a few variables that have the original base url still
    sedas.sensor_url = f"{sedas.base_url}sensors"
    sedas.authentication_url = f"{sedas.base_url}authentication"
    sedas.search_url = f"{sedas.base_url}search"

    # Get rid of the token force the log in to happen again.
    sedas._token = None  

    # now we can get the users actual test password
    sedas._username = input("Please enter your test username:")
    sedas.__password = getpass("Please enter your test password:")
    # and log into test
    sedas.login()

    # now what ever end points we call should go to the test server.
    result_sats = sedas.list_satellites()

    ## do some thing a bit more interesting with the results.
    print(json.dumps(result_sats, sort_keys=True, indent=4, separators=(',', ': ')))

    satellites = []
    for i in range(0, len(result_sats)):
        satellites.append(result_sats[i]['name'])

    print(f"Available satellites are: {', '.join(satellites)}")
