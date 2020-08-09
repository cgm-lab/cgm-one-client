import socket


def get_server_ip(domains=["one.cgm.im", "cgm.cs.ntust.edu.tw", "cgm.im"]) -> str:
    for d in domains:
        try:
            ip = socket.gethostbyname(d)
            if ip.startswith("140.118"):
                return ip
        except Exception:
            pass

    raise ValueError(f"{domains} is not in NTUST (140.118.x.y)")
