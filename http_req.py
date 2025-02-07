import base64
import concurrent.futures
import re
import requests
from set_proxy import proxies


def get_response(url):
    response = requests.get(
        url, timeout=10, headers={"User-Agent": "v2rayNG/*.*.*"}, proxies=proxies
    )
    response = response.text
    links = []
    if any(proto in response for proto in ["vmess:", "trojan:", "vless:"]):
        links.extend(response.splitlines())
    elif any(proto in response for proto in ["http:", "https:"]):
        url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
        sub_urls = re.findall(url_pattern, response)
        links = get_responses(sub_urls)
    else:
        decoded_line = base64.b64decode(response).decode("utf-8")
        if any(proto in decoded_line for proto in ["vmess:", "trojan:", "vless:"]):
            links.extend(decoded_line.splitlines())
    return links


def get_responses(urls):
    links = []

    def process(url):
        sub_response = requests.get(
            url, timeout=10, headers={"User-Agent": "v2rayNG/*.*.*"}, proxies=proxies
        )
        sub_response = sub_response.text
        if any(proto in sub_response for proto in ["vmess:", "trojan:", "vless:"]):
            links.extend(sub_response.splitlines())
        else:
            try:
                decoded_line = base64.b64decode(sub_response).decode("utf-8")
                if any(
                    proto in decoded_line for proto in ["vmess:", "trojan:", "vless:"]
                ):
                    links.extend(decoded_line.splitlines())
            except Exception as e:
                print(e)

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(process, urls)
    return links
