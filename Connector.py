#!/usr/bin/python
# coding: utf-8
import logging
import os
import pdb
import traceback

import paramiko
import logging.config

import time

import scriptinfo
from tools import Tools as tool
from DAO import DAO as dao


class Connctor:
    def __init__(self):
        self.conn = None
        self.conn_info = {}
        logging.config.fileConfig("etc/logging.conf")
        self.logger = logging.getLogger("scriptstool")
        self.result = []
        self.create_time = None
        self.update_time = None
        self.tool = tool
        self.dao = dao

    def run_script(self, fp, env, script_name):
        status = self.dao.get_status(script_name, env)
        if status != "1":
            self.execute_cmd(fp, env, script_name)
        else:
            return status

    # 创建sshclient连接服务器,执行命令
    def execute_cmd(self, env, fp, script_name):
        self.logger.info("env:{},script_name:{}".format(env, script_name))
        # 获取环境信息
        self.get_conn_info(env)
        conn_info = self.conn_info
        execmd = self.splice_cmd(env, script_name, fp)

        # 检查是否能连通
        ping_result = self.check_ping(conn_info["hostname"])
        if isinstance(ping_result, int):
            self.logger.info(conn_info)
            script_id = dao().get_script_info(env, script_name).id
            createtime = time.time()
            dao().update_reslut_createtime(script_id, createtime)
            self.tool.encode_fac(conn_info)
            self.result = self.create_client(conn_info["hostname"], conn_info["port"], conn_info["username"],
                                             conn_info["password"], execmd)
            updatetime = time.time()
            script_id = dao().get_script_info(env, script_name).id
            self.logger.info("result:{}".format(self.result))
            data = self.processing_results(env=env, script_name=script_name, resluts=self.result, fp=fp)
            dao().create_resluts(script_name, script_id, data, env, createtime, updatetime)
            return data
        else:
            return ping_result

    def processing_results(self, env, script_name, resluts, fp):
        item = ["当前执行的环境为:{}".format(self.conn_info["environment"]),
                "执行的脚本为:{}".format(scriptinfo.script_data[script_name][0]),
                "脚本名称:{}".format(scriptinfo.script_data[script_name][1]),
                "执行的结果为:{}".format(resluts)]
        if env == "Intranet":

            # noinspection PyTypeChecker
            item.insert(2, "当前执行的机器为:{}".format(fp))
            resluts = "\n".join(item)
            return resluts
        elif env == "Outside":
            resluts = "\n".join(item)
            return resluts

    # 获取链接详细
    def get_conn_info(self, env):
        self.conn = dao().get_connection_info(env)
        self.logger.info("env_hosts type:{}".format(type(self.conn.env_hosts)))
        self.conn_info["hostname"] = self.conn.env_hosts
        self.conn_info["password"] = self.conn.env_password
        self.conn_info["username"] = self.conn.env_username
        self.conn_info["port"] = self.conn.env_port
        self.conn_info["environment"] = self.conn.env_info

    # 拼接command
    def splice_cmd(self, env, script_name, fp):
        execmd = dao().get_script_info(env, script_name).script_content
        if env == "Intranet":
            execmd = execmd.format(fp)
            if script_name is "ABtest":
                execmd = "{}{}{}".format(
                    tool().replace_file("/usr/local/webdata/php/{}/fun/batch/Betatest".format(fp),
                                        "mysql:host=192.168.100.60;",
                                        "mysql:host=192.168.100.78;", "config.php"), "\n", execmd)
        return execmd

    # 创建client
    def create_client(self, hostname, port, username, password, execmd):

        self.logger.info("start connect to SSHClient")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.logger.info(
            "connect info host:{} username:{} password:{} port:{} execmd:{}".format(hostname, username, password, port,
                                                                                    execmd))

        client.connect(hostname, port, username, password)
        self.create_time = time.time()
        stdin, stdout, stderr = client.exec_command(execmd)
        txt = stdout.read()
        self.logger.info("success connect to SSHClient,start to execute command")
        client.close()
        self.update_time = time.time()

        return txt

    # 检查是否可以连上目标服务器
    def check_ping(self, hostname):
        ping_result = os.system('ping -c 1 ' + hostname)
        self.logger.debug("start to check ping :{}".format(hostname))
        if ping_result == 0:
            return ping_result
        else:
            return 'Can not ping through {}!!!!'.format(hostname)

            # def close_conn(self):
            #     if self.conn is not None: self.conn.close()

    # 拼接html table详细信息
    def get_html_table(self):
        table = []
        item = self.get_table_info()
        print item
        for tem in item:
            print tem
            status = self.change_status_to_chinese(tem["ScriptStatus"])

            tr ="<tr>" \
                    "<td>" + tem["ScriptInfo"] + "</td>" \
                    "<td class='" + tem["ScriptInfo"] + "_status    '>" + status + "</td>" \
                    "<td class='tab .thead .right'>" \
                        "<button class='" + tem["ScriptName"] + "' value='Intranet'>内测</button> " \
                        "<button class='" + tem["ScriptName"] + "'value='Outside'>外测</button> " \
                        "<button class='" + tem["ScriptName"] + "'>查看结果</button>" \
                    "</td>" \
                "</tr>"
            table.append(tr)
        table = "\n".join(table)
        return table

    # 检查运行状态
    def check_script_status(self, script_name, env):

        update_time = self.dao.get_updatetime(script_name)
        create_time = self.dao.get_createtime(script_name)
        try:
            if update_time <= create_time:
                self.dao.update_script_status(script_name, env, status=1)
            elif update_time > create_time:
                self.dao.update_script_status(script_name, env, status=2)
            else:
                self.dao.update_script_status(script_name, env, status=0)
        except:
            print traceback.print_exc()

    # 获取脚本列表的详细信息
    def get_table_info(self):
        table_info = []
        script_data = dao().get_all_script_info()
        for index in range(script_data.__len__()):
            item = {}
            tem = script_data[index].get_all()
            print tem
            item["ScriptName"] = tem["short_name"]
            item["ScriptInfo"] = tem["script_info"]
            item["ScriptStatus"] = tem["script_status"]

            table_info.append(tool().encode_fac(item))
        print "##############"
        print table_info
        print "##############"
        return table_info

    def change_status_to_chinese(self,status):
        if status == 0:
            status = "未执行"
        elif status == 1:
            status = "执行中"
        elif status == 2:
            status = "已完成"
        return status
if __name__ == '__main__':
    conn = Connctor()
    # hostname = "192.168.74.12"
    # username = "qa"
    # port = 22
    # password = "fanliqa"
    # execmd = "cd /usr/local/webdata/php/fp156/fun/batch/Betatest \n sed -i 's/mysql:host=192.168.100.60;/mysql:host=192.168.100.78;/' config.php \n cat config.php"
    # txt = conn.execute_cmd()
    # print txt
    env = "Intranet"
    fp = "fp156"
    script_name = "Super"
    conn.execute_cmd(env=env, fp=fp, script_name=script_name)
    # print conn.get_html_table()
    # print conn.splice_cmd("Intranet","ABtest","fp156")
