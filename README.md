# Linux to Telegram backup

Send your Linux directories/files from multiple servers to any telegram chat

You can deploy this project on your personal computer/server or any CI/CD platform you wish.

<h3>Instructions for self-host</h3>

1. Clone the repository or download the source code.

```
git clone https://github.com/EryX0/Linux-to-Telegram-backup.git
```

2. open the cloned repo, (ex. on linux):

```
cd Linux-to-Telegram-backup
```

3. install the requirements

```
pip install -r requirements.txt
```

4. run the setup.py application (just one time to generate the config file) and fill out the needed info

```
python3 setup.py
```

5. run the main application
```
python3 main.py
```

**or** set a cronjob to run it periodically (only the main.py), [tutorial for setting cronjob here](https://towardsdatascience.com/how-to-schedule-python-scripts-with-cron-the-only-guide-youll-ever-need-deea2df63b4e).

docker image is also available [Here](https://hub.docker.com/repository/docker/eryx0/linux-to-telegram-backup/general), guide for docker deployment is soon to be added.
