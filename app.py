import socket

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from client import get_all_metrics
from utils import get_server_ip

SERVER_IP = get_server_ip()

app = FastAPI()


@app.middleware("http")
async def source_host_check(request, call_next):
    """Only allow CGM Lab server"""
    ip = request.client.host
    if ip not in ["127.0.0.1", SERVER_IP]:
        print(ip, "is not allowed!")
        return JSONResponse({}, status_code=status.HTTP_403_FORBIDDEN)
    response = await call_next(request)
    return response


@app.get("/api")
async def main():
    metrics = get_all_metrics()
    return metrics


if __name__ == "__main__":
    print(f"Server IP: {SERVER_IP}")
    uvicorn.run(app, host="0.0.0.0", port=9999)
