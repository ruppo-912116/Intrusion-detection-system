#! /bin/sh 

pip install watchdog

cd /home/detectionscript


read -p 'Email: ' uservar
read -sp 'Password: ' passvar


nohup python detection.py /var/log/nginx/error.log uservar passvar >> detection.log &


 
