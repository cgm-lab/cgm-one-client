import socket
import sys
import time

import requests
import schedule

from client import get_all_metrics, get_ip

URL = "https://one.cgm.im"
if get_ip().startswith("192.168"):
    URL = "http://192.168.10"


class Host:
    def __init__(self):
        self.metrics = get_all_metrics()

    def is_registed(self) -> bool:
        res = requests.get(f"{URL}/api/hosts")
        return self.metrics["ip"] in res.json()

    def register(self) -> bool:
        res = requests.post(
            f"{URL}/api/hosts",
            json=self.metrics,
        )
        return res.ok

    def deregister(self) -> bool:
        res = requests.delete(f"{URL}/api/hosts")
        return res.ok

    def update_metrics(self) -> bool:
        self.metrics = get_all_metrics()
        res = requests.put(f"{URL}/api/hosts", json=self.metrics)
        return res.ok


def process(host) -> bool:
    print("Start processing...")
    if not host.is_registed():
        if host.register():
            print("Register successful!")
            return True
        print("Register fail!")
        return False
    if host.update_metrics() or host.update_metrics():
        print("Update data success!!")
        return True
    print("Update data fail!")
    return True


if __name__ == "__main__":
    try:
        host = Host()
        process(host=host)
        schedule.every(5).minutes.at(":00").do(process, host=host)
        while True:
            schedule.run_pending()
            time.sleep(1)
        pass
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        ok = host.deregister()
        if ok:
            print("Deregister success!")
        else:
            print("Deregister fail!")
