import json

import concurrent.futures

from urllib.request import Request
from urllib.request import urlopen


def call_api(url):
    req = Request(url)
    response = urlopen(req)
    return json.loads(str(response.read(), "utf-8"))

def get_contents(urls):
    contents = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(call_api, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                contents.append({
                    "url" : url,
                    "response": data
                })
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
    return contents

def run():
    URL = "https://soda.demo.socrata.com/resource/earthquakes.json"
    LIMIT = 10
    MAX_LIMIT = 100
    urls = []
    offset = 0
    while offset < MAX_LIMIT:
        urls.append("%s?$limit=%s&$offset=%d" % (URL, LIMIT, offset))
        offset += LIMIT
    
    print(get_contents(urls))
    print("Finished !")

if __name__ == "__main__":
    run()