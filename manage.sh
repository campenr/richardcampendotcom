#!/bin/bash
args="$@"
vagrant ssh -c "cd /home/vagrant/wagtailsite/app && source /home/vagrant/venv/wagtailsite/bin/activate && python /home/vagrant/wagtailsite/app/manage.py $args"
