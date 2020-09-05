## Kodi backup script

```
cd /home/osmc
sudo apt-get update && sudo apt-get install -y python3-pip python3-venv cron git
git clone https://github.com/kutny/kodi_backup.git
cd kodi_backup
AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=yyy ./setup.sh
```
