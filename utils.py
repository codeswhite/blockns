def download_blocklist(source):
    from urllib.request import urlopen
    from time import time

    # try: TODO
    with urlopen(source) as stream:
        last_time = time()
        data = stream.read().decode()
    return data, time() - last_time


def prompt():
    try:
        input()
        return True
    except KeyboardInterrupt:
        exit(-1)
