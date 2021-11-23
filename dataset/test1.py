import requests
import json
import time
from datetime import datetime
from threading import Thread

consumer_key = "9R7ST3BHb3Em1nh5E43iRc7ip"  # Add your API key here
consumer_secret = "88lpbfyhfo0ovD5orQf5dQ0WS35QkAxCDPvBYnx6bQl5JXWnfi"  # Add your API secret key here
records_per_file = 5000  # Replace this with the number of tweets you want to store per file
file_path = "dataset/"  # Replace with appropriate file path followed by / where you want to store the file

count = 0
file_object = None
file_name = None


def get_bearer_token(key, secret):
    response = requests.post(
        "https://api.twitter.com/oauth2/token",
        auth=(key, secret),
        data={'grant_type': 'client_credentials'},
        headers={"User-Agent": "TwitterDevCovid19StreamQuickStartPython"})

    if response.status_code != 200:
        raise Exception(f"Cannot get a Bearer token (HTTP %d): %s" % (response.status_code, response.text))

    body = response.json()
    return body['access_token']


# Helper method that saves the tweets to a file at the specified path
def save_data(item):
    global file_object, count, file_name
    if file_object is None:
        file_name = int(datetime.utcnow().timestamp() * 1e3)
        count += 1
        file_object = open(f'{file_path}covid19-{file_name}.csv', 'a')
        file_object.write("{}\n".format(item))
        return
    if count == records_per_file:
        file_object.close()
        count = 1
        file_name = int(datetime.utcnow().timestamp() * 1e3)
        file_object = open(f'{file_path}covid19-{file_name}.csv', 'a')
        file_object.write("{}\n".format(item))
    else:
        count += 1
        file_object.write("{}\n".format(item))


def stream_connect(partition):
    response = requests.get("https://api.twitter.com/labs/1/tweets/stream/covid19?partition={}".format(partition),
                            headers={"User-Agent": "TwitterDevCovid19StreamQuickStartPython",
                                     "Authorization": "Bearer {}".format(
                                         "AAAAAAAAAAAAAAAAAAAAAPU0UwEAAAAAhG8SdTO3Qvsvfyfg3DgV%2Fa2BimE%3DjU3KQzVX14QncIuEgpSynzS9B5nIoPRB379IJL7bN7o4daV5nM")},
                            stream=True)
    for response_line in response.iter_lines():
        if response_line:
            save_data(json.loads(response_line))


def main():
    timeout = 0
    while True:
        for partition in range(1, 5):
            Thread(target=stream_connect, args=(partition,)).start()
        time.sleep(2 ** timeout * 1000)
        timeout += 1


if __name__ == "__main__":
    main()