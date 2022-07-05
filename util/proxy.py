import os


def init_proxy():
    os.environ['http_proxy'] = "http://localhost:7890"
    os.environ['HTTP_PROXY'] = "http://localhost:7890"
    os.environ['https_proxy'] = "http://localhost:7890"
    os.environ['HTTPS_PROXY'] = "http://localhost:7890"
