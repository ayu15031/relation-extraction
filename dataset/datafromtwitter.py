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
        file_object = open(f'{file_path}covid19-{file_name}.json', 'a')
        file_object.write("{}\n".format(item))
        return
    if count == records_per_file:
        file_object.close()
        count = 1
        file_name = int(datetime.utcnow().timestamp() * 1e3)
        file_object = open(f'{file_path}covid19-{file_name}.json', 'a')
        file_object.write("{}\n".format(item))
    else:
        count += 1
        file_object.write("{}\n".format(item))


def stream_connect():
    data = []
    response = requests.get("https://api.twitter.com/2/tweets/search/recent?query=covid19,us", headers={"Authorization": "Bearer {}".format(get_bearer_token(consumer_key, consumer_secret))})
    for response_line in response.iter_lines():
        if response_line:
            data.extend(json.loads(response_line)['data'])
    response = response.json()
    i = 0

    while 'next_token' in response['meta'] and response['meta']['next_token'] != '':
        try:
            next = response['meta']['next_token']
            response = requests.get(f"https://api.twitter.com/2/tweets/search/recent?query=(covid19)lang:en&next_token={next}&max_results=100", headers={"Authorization": "Bearer {}".format(get_bearer_token(consumer_key, consumer_secret))})
            for response_line in response.iter_lines():
                if response_line:
                    data.extend(json.loads(response_line)['data'])
                # for line in a:
                    
                
                # 
            response = response.json()
            print(f"----------------- iteration {i} ---------------")
            i+=1
            if i == 1000:
                break

            print(response['meta'])
        except Exception as e:
            print(f"An error was encountered: {e}")
            print(response)
            break
            


    # dataset = json.loads(data)
    print(len(data))
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    # print(response.json()['meta'])
    



def main():
    stream_connect()
    # timeout = 0
    # while True:
    #     for partition in range(1, 5):
    #         Thread(target=stream_connect, args=(partition,)).start()
    #     time.sleep(2 ** timeout * 1000)
    #     timeout += 1


if __name__ == "__main__":
    main()