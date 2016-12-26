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
    return "done"

@app.route("/get_table_info", methods=['GET'])
def get_table_info():
    html = connector.get_html_table(None)
    return html


@app.route("/get_script_status", methods=['POST'])
def get_scripts_status():
    script_name = request.form.get("scrip_name")
    env = request.form.get("env")
    status = connector.check_script_status(script_name, env)
    return str(status)


@app.route("/get_result_page", methods=['POST'])
def get_result_page():
    script_name = request.form.get("script_name")
    result = connector.get_result_page(script_name)
    return result

@app.route("/create_scirpt", methods=['POST'])
def create_scirpt():
    script_info = request.form.get("script_info")
    script_path = request.form.get("script_path")
    script_data = {
        "script_info": script_info,
        "script_path": script_path
    }
    print script_data
    hint = connector.create_php_script(script_data)
    print hint
    return hint

@app.route("/edit_scirpt", methods=['POST'])
def edit_scirpt():
    script_name = request.form.get("script_name")
    script_info = request.form.get("script_info")
    script_content_n = request.form.get("script_content_n")
    script_content_o = request.form.get("script_content_o")
    script_data = {
        "script_name": script_name,
        "script_info": script_info,
        "script_content_o": script_content_o,
        "script_content_n": script_content_n,
    }
    hint = connector.edit_php_script(script_data)
    return hint

@app.route("/get_newpage_info", methods=['GET'])
def get_newpage_info():
    html = connector.get_newpage_table(None)
    return html

@app.route("/search", methods=['POST'])
def search():
    name = request.form.get("name")
    page = request.form.get("page")
    print name
    html = connector.get_search(name,page)
    return html

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)
