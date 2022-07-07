import requests

controller = "http://127.0.0.1:9090/proxies/"
proxy_url = controller + "AmyTelecom"

proxy_group = [
    '香港 01', '香港 HK 02', '香港 HK 03', '香港 HK 04', '香港 HK 05', '香港 HK 06', '香港 HK 07', '香港 HK 08', '香港 HK 09',
    '香港 HK 10'
]


def change_proxy(current_cid):
    current_cid = (current_cid + 1) % len(proxy_group)
    proxy_name = proxy_group[current_cid]
    print("Change proxy: " + proxy_name)
    r = requests.put(proxy_url, json={"name": proxy_name})
    print(r.status_code)
    return current_cid


if __name__ == "__main__":
    current_cid = 1
    current_cid = change_proxy(current_cid)
    print(current_cid)
