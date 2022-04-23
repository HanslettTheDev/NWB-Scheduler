import re
from flask import Flask, render_template, request, redirect, flash, url_for, session
from nwb import app, db

from nwb.utils import UTILS
from nwb.models import NWBDATA, get_data, POSTS
from nwb.forms import MonthSelector

utils = UTILS()

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    # scrap data first
    # scrap = utils.scrap_data(27,18)
    return render_template('main.html')

@app.route('/editor-nwb', methods=['GET', 'POST'])
def editor():
    data = get_data('April')
    return render_template('editor.html', data=data)

@app.route('/schedule', methods=['GET', 'POST'])
def program():
    data = get_data('February')
    return render_template('schedule.html')