import os
import socket
from datetime import datetime

import GPUtil as gputil
import psutil
import requests

units = {"TB": 1024 ** 4, "GB": 1024 ** 3, "MB": 1024 ** 2, "KB": 1024 ** 1}

# TODO: domain lookup


def get_all_metrics(unit: str = "GB"):
    metrics = {
        "os": get_os_platform(),
        "ip": get_ip(),
        "cpu": get_cpu_usage(),
        "ram": get_virtual_memory(unit),
        "disks": get_disks_space(unit),
        "vram": get_gups_vram(unit),
        "net": get_ntust_net_usage(unit),
    }
    if not metrics["net"]:
        del metrics["net"]
    return metrics


# OS
def get_os_platform() -> str:
    from sys import platform as pf

    if pf.startswith("win"):
        from platform import system, version

        return system() + " " + version()
    elif pf == "darwin":
        from plistlib import load

        d = load(open("/System/Library/CoreServices/SystemVersion.plist", "rb"))
        return d["ProductName"] + " " + d["ProductUserVisibleVersion"]
    elif pf == "linux":
        return next(
            filter(lambda l: "PRETTY_NAME" in l, open("/etc/os-release").readlines())
        ).split('"')[1]
    raise NotImplementedError(pf)


# CPU
def get_cpu_usage():
    return {"total": 100, "used": psutil.cpu_percent(interval=1), "unit": "%"}


# RAM
def get_virtual_memory(unit: str = "GB"):
    ram = psutil.virtual_memory()
    total = ram.total
    used = ram.total - ram.available
    total /= units[unit]
    used /= units[unit]
    return {"total": total, "used": used, "unit": unit}


# DISK space
def get_disks_space(unit: str = "GB"):
    parts = list(filter(lambda p: "rw" in p.opts, psutil.disk_partitions()))
    disks = {}
    for p in parts:
        disk = psutil.disk_usage(p.mountpoint)
        # Greater than 20G
        if disk.total > 20 * 1024 ** 3:
            disks[p.mountpoint] = {
                "total": disk.total / units[unit],
                "used": disk.used / units[unit],
                "unit": unit,
            }

    return disks


def get_gups_vram(unit: str = "GB"):
    gpus = {}
    for gpu in gputil.getGPUs():
        gpus[f"{gpu.id}: {gpu.name}"] = {
            "total": gpu.memoryTotal * 1024 * 1024 / units[unit],
            "used": gpu.memoryUsed * 1024 * 1024 / units[unit],
            "unit": unit,
        }
    return gpus


# Get IP
def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    if ip.startswith("140.118") or ip.startswith("192.168"):
        return ip
    return ""


# Get NTUST network usage
def get_ntust_net_usage(unit: str = "GB"):
    ip = get_ip()
    if ip == "192.168.0.10":  # DMZ
        ip = "140.118.9.222"
    elif not ip or not ip.startswith("140.118"):
        print("IP not in school")
        return {}
    res = requests.post(
        "https://network.ntust.edu.tw/flowStatistics/getFlowData",
        {"ip": ip, "dt": str(datetime.today().date()), "units": "0"},
    )
    try:
        network = res.json()["items"][0]
        used = network["totflow"]
        # convert str -> int
        used = int("".join(filter(str.isdigit, used)))
        used /= units[unit]
    except Exception as e:
        print(e)
        return {"total": 1, "used": 0, "unit": "?"}
    return {"total": 20, "used": used, "unit": unit}


if __name__ == "__main__":
    print(get_all_metrics())
