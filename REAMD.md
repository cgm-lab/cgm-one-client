# CGM One Monitor API

## Setup

Clone repo

```bash
git clone {} ~/cgm-one-monitor-api
```

Install `requirements.txt`

```bash
pip install requirements.txt
```

## Run

```bash
uvicorn app:app --host 0.0.0.0 --port 9999
```

or

```bash
python app.py
```

## Service

- Linux
  - Copy file from `service/cgm-one-monitor-api.service` to `/etc/systemd/system/cgm-one-monitor-api.service`
  - Modify user name
  - <https://askubuntu.com/a/919059>
- Windows
  - Copy file from `service/cgm_one_monitor_api.bat` to path `[D|C]:\Users\{User}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` or `shell:common startup`
  - <https://stackoverflow.com/questions/21218346/run-batch-file-on-start-up>
