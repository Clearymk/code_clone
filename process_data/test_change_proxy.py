import requests

controller = "http://127.0.0.1:2390/proxies/"
proxy_url = controller + "%F0%9F%9A%80%20%E8%8A%82%E7%82%B9%E9%80%89%E6%8B%A9"

proxy_group = [
    '台湾 TW 01', '台湾 TW 02', '台湾 TW 03', '台湾 TW 04', '台湾 TW 05', '台湾 TW 06', '台湾 TW 07', '台湾 TW 08',
    '新加坡 SG 01', '新加坡 SG 02', '新加坡 SG 03', '新加坡 SG 04', '新加坡 SG 05', '新加坡 SG 06', '新加坡 SG 07', '新加坡 SG 08',
    '日本 JP 01', '日本 JP 02', '日本 JP 03', '日本 JP 04', '日本 JP 05', '日本 JP 06', '日本 JP 07', '日本 JP 08',
    '韩国 KR 01', '韩国 KR 02', '韩国 KR 03', '韩国 KR 04', '韩国 KR 05', '韩国 KR 06', '韩国 KR 07', '韩国 KR 08',
    '香港 HK 01', '香港 HK 02', '香港 HK 03', '香港 HK 04', '香港 HK 05', '香港 HK 06', '香港 HK 07', '香港 HK 08', '香港 HK 09',
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
