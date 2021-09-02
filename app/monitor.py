#!/usr/bin/python3
import datetime
import os
import platform
import psutil
from flask import *
from app import app

import config1 as cfg
from app import info

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    target = os.path.join(APP_ROOT, 'static/')
    active_since = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    return render_template("monitor.html",
                           script_version=cfg.version,
                           active_since=active_since,
                           system=platform.system(),
                           release=platform.release(),
                           version=platform.version(),
                           blocks=info.get_blocks(), title='monitor')
