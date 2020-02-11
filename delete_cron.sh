# Delete outdated notices from DB
cd /home/ubuntu/EwhaNoticeServer
.venv/bin/python3 delete.py

# Delete log
rm /home/ubuntu/cron.log
cat /home/ubuntu/cron.log
