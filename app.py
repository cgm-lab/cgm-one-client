import socket
import sys
import time

import requests
import schedule

from client import get_all_metrics

SERVER = "one.cgm.im"


class Host:
    def __init__(self):
        self.metrics = get_all_metrics()

    def is_registed(self) -> bool:
        res = requests.get(f"https://{SERVER}/api/hosts")
        return self.metrics["ip"] in res.json()

    def register(self) -> bool:
        res = requests.post(
            f"https://{SERVER}/api/hosts",
            json=self.metrics,
        )
        return res.ok

    def deregister(self) -> bool:
        res = requests.delete(f"https://{SERVER}/api/hosts")
        return res.ok

    def update_metrics(self) -> bool:
        self.metrics = get_all_metrics()
        res = requests.put(f"https://{SERVER}/api/hosts", json=self.metrics)
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