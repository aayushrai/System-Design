#!/bin/bash
# source venv/faceRecog/bin/activate
gnome-terminal -e 'bash -c "gunicorn --bind 127.0.0.1:6001 server:app"' &
gnome-terminal -e 'bash -c "gunicorn --bind 127.0.0.1:6002 server:app"' &
gnome-terminal -e 'bash -c "gunicorn --bind 127.0.0.1:6003 server:app"' &
gnome-terminal -e 'bash -c "gunicorn --bind 127.0.0.1:6004 server:app"'

# gunicorn --bind 127.0.0.1:6000 facerecogSlave:app &
# gunicorn --bind 127.0.0.1:6001 facerecogSlave:app 