#!/usr/bin/python
# coding: utf-8

from flask import Flask
from flask import render_template
from flask import request

import Connector

app = Flask(__name__)


def __init__(self):
    pass


connector = Connector.Connctor()


# welcome page
@app.route('/')
def index():
    return render_template('index.html')


@app.route("/run_scrip", methods=['POST'])
def run_scrip():
    fp = request.form.get("fp")
    env = request.form.get("env")
    script_name = request.form.get("scrip_name")
    connector.run_script(env=env, fp=fp, script_name=script_name)


@app.route("/get_table_info", methods=['GET'])
def get_table_info():
    html = connector.get_html_table()
    return html


@app.route("/get_scripts_status", methods=['POST'])
def get_scripts_status():
    script_name = request.form.get("scrip_name")
    env = request.form.get("env")
    status = connector.check_script_status(script_name, env)
    return status


@app.route("/get_result_page", methods=['POST'])
def get_result_page():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
