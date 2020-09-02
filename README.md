# CGM One Monitor Client

## Setup

Clone repo

```bash
cd ~  # Go to home
git clone https://github.com/cgm-lab/cgm-one-client.git ./cgm-one-client
```

Install `requirements.txt`

```bash
cd cgm-one-client
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## Service

- Linux
  - Copy file from `service/cgm-one-client.service` to `/etc/systemd/system/cgm-one-client.service`
  - Modify user name
  - ufw firewall `sudo ufw allow proto tcp from 140.118.0.0/16 to any port 9999`
  - <https://askubuntu.com/a/919059>
- Windows
  - Disable `Quick Edit mode` in CMD
  - Copy file from `service/cgm-one-client.bat` to path `[D|C]:\Users\{User}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` or `shell:common startup`
  - <https://stackoverflow.com/questions/21218346/run-batch-file-on-start-up>
