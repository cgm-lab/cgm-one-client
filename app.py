import socket
import sys
import time

import requests
import schedule

from client import get_all_metrics

SERVER = "one.cgm.im"


class Service:
    token: str = ""

    def push(self):
        metrics = get_all_metrics()
        requests.post(f"https://{SERVER}/metrics/{self.token}")

    def is_registed(self) -> bool:
        if not self.token:
            return False
        # TODO: send reqeuest to check this token is valid
        return True

    def register(self) -> bool:
        res = requests.post(f"https://{SERVER}/register")
        # TODO: get token
        self.token = ""

    def deregister(self) -> bool:
        res = requests.delete(f"https://{SERVER}/register")


def process(svc) -> bool:
    if not svc.is_registed():
        if not svc.register():
            print("Service register fail!")
            return False
    if svc.push() or svc.push():
        print("Push data success!!")
        return True
    print("Push data fail!")
    return True


if __name__ == "__main__":
    try:
        svc = Service()
        schedule.every(5).minutes.at(":00").do(process, svc=svc)
        while True:
            schedule.run_pending()
            time.sleep(1)
        pass
    except KeyboardInterrupt:
        print("Stopping")
    finally:
        svc.deregister()
