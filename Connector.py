#!/usr/bin/python
# coding: utf-8
import logging
import os
import pdb
import threading
import traceback

import paramiko
import logging.config

import time

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
        self.logger.info("start to run script: script_name is {}, env is {}".format(script_name, env))
        status = self.dao().get_status(script_name)
        if status != 1:
            status = 1
            self.logger.info("set {} status to {}".format(script_name,status))
            self.dao().update_script_status(script_name,status)
            try:
                self.execute_cmd(env, fp, script_name)
                status = 2
                self.dao().update_script_status(script_name,status)
                self.logger.info("set {} status to {}".format(script_name,status))
            except Exception,e:
                status = 3
                self.dao().update_script_status(script_name,status)
                self.logger.info("set {} status to {}".format(script_name,status))
                print Exception, ":", e
        else:
            self.logger.info("status is running, so skip")
            return status

    # 创建sshclient连接服务器,执行命令
    def execute_cmd(self, env, fp, script_name):
        self.logger.info("start to execute_cmd env:{},script_name:{}".format(env, script_name))
        # 获取环境信息
        self.get_conn_info(env)
        conn_info = self.conn_info
        execmd = self.splice_cmd(env, script_name, fp)

        # 检查是否能连通
        ping_result = self.check_ping(conn_info["hostname"])
        if isinstance(ping_result, int):
            self.logger.info(conn_info)
            script_id = dao().get_script_info(script_name).id
            createtime = time.time()
            dao().update_reslut_createtime(script_id, createtime)
            self.tool().encode_fac(conn_info)
            self.result = self.create_client(conn_info["hostname"], conn_info["port"], conn_info["username"],
                                             conn_info["password"], execmd)
            updatetime = time.time()
            dao().update_reslut_updatetime(script_id, updatetime)
            script_id = dao().get_script_info(script_name).id
            self.logger.info("result:{}".format(self.result))
            data = self.processing_results(env=env, script_name=script_name, resluts=self.result, fp=fp)
            dao().create_resluts(script_name, script_id, data, env, createtime, updatetime)
            self.logger.info("data {}".format(data))
        else:
            return ping_result

    def processing_results(self, env, script_name, resluts, fp):
        info = self.get_script_info_by_name(script_name)
        item = ["当前执行的环境为: {}".format(self.conn_info["environment"]),
                "执行的脚本为: {}".format(info["info"]),
                "脚本名称: {}".format(info["name"]),
                "执行的结果为: {}".format(resluts)]
        if env == "Intranet":
            # noinspection PyTypeChecker
            item.insert(2, "当前执行的机器为:{}".format(fp))
            resluts = "<br>".join(item)
            return resluts
        elif env == "Outside":
            resluts = "<br>".join(item)
            return resluts

    # 获取链接详细
    def get_conn_info(self, env):
        self.conn = dao().get_connection_info(env)
        self.conn_info["hostname"] = self.conn.env_hosts
        self.conn_info["password"] = self.conn.env_password
        self.conn_info["username"] = self.conn.env_username
        self.conn_info["port"] = self.conn.env_port
        self.conn_info["environment"] = self.conn.env_info

    # 拼接command
    def splice_cmd(self, env, script_name, fp):
        if env =="Intranet":
            execmd = dao().get_script_info(script_name).script_content_n
        elif env == "Outside":
            execmd = dao().get_script_info(script_name).script_content_o
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
        last_item = self.get_last_script()
        result_scriptname = self.get_result_scriptname()
        for tem in item:
            status = self.change_status_to_chinese(tem["ScriptStatus"])
            env = "Intranet"
            if tem["ScriptName"] in result_scriptname:
                env = last_item[result_scriptname.index(str(tem["ScriptName"]))][0]
                # status += last_item[1][last_item[0].index(self.tool().encode_fac(tem["ScriptName"]))]
            tr ="<tr>" \
                    "<td>" + tem["ScriptInfo"] + "</td>" \
                    "<td class='"+ tem["ScriptName"]+"_name'>"+tem["scriptdetail"]+"</td>"\
                    "<td class='"+ tem["ScriptName"] + "_status'>" + self.tool().encode_fac(status) +"("+self.tool().encode_fac(self.change_env_to_chinese(env))+")"+ "</td>" \
                    "<td class='tab .thead .right'>" \
                        "<button class='" + tem["ScriptName"] + "' value='Intranet'>内测</button> " \
                        "<button class='" + tem["ScriptName"] + "'value='Outside'>外测</button> " \
                        "<button href='#modal-table' role='button' class='"+tem["ScriptName"]+"' data-toggle='modal'>查看结果</button>"\
                    "</td>" \
                "</tr>"
            table.append(tr)
        table = "\n".join(table)
        return table

    # 检查运行状态
    def check_script_status(self, script_name, env):
        self.logger.info("start to check script status,script_name:{} env:{}".format(script_name,env))
        # update_time = float(self.dao().get_updatetime(script_name))
        # create_time = float(self.dao().get_createtime(script_name))
        # if update_time <= create_time:
        #     status = 1
        #     self.dao().update_script_status(script_name, env, status)
        # elif update_time > create_time:
        #     status = 2
        #     self.dao().update_script_status(script_name, env, status)
        # else:
        #     status = 0
        #     self.dao().update_script_status(script_name, env, status)
        # return self.change_status_to_chinese(status)
        status = self.dao().get_status(script_name)
        self.logger.info("get {} status in {}, status is {}".format(script_name, status, env))
        status = self.change_status_to_chinese(status) +"("+self.change_env_to_chinese(env)+")"
        return status
    # 获取脚本列表的详细信息
    def get_table_info(self):
        table_info = []
        script_data = dao().get_all_script_info()
        for index in range(script_data.__len__()):
            item = {}
            tem = script_data[index].get_all()
            item["ScriptName"] = tem["short_name"]
            item["ScriptInfo"] = tem["script_info"]
            item["ScriptStatus"] = self.change_status_to_chinese(tem["script_status"])
            item["scriptdetail"] = tem["script_detail"]
            table_info.append(tool().encode_fac(item))

        return table_info

    def change_status_to_chinese(self,status):
        if status == 0:
            status = "未执行"
        elif status == 1:
            status = "执行中"
        elif status == 2:
            status = "已完成"
        elif status == 3:
            status = "执行失败,请重试"
        return status

    def change_env_to_chinese(self,env):
        if env == "Intranet":
            env = "内测"
        elif env == "Outside":
            env = "外测"
        return env

    def get_result_scriptname(self):
        scriptname_list = []
        item = self.get_last_script()
        for index in range(item.__len__()):
            scriptname_list.append(item[index][1])
        return scriptname_list

    def get_last_script(self):
        results_data = self.dao().get_last_script()
        data = []
        for index in range(results_data.__len__()):
            item = []
            tem = results_data[index].get_all()
            item.append(tem["env"])
            item.append(tem["scripts_name"])
            data.append(item)
        return data

    def get_result_page(self,script_name):
        item = self.tool().encode_fac(self.get_result_data(script_name))

        table_info =\
            "<tr>\
                <td>脚本名称</td>\
                <td>"+item["script_name"]+"</td>\
            </tr>\
            <tr>\
                <td>执行时间</td>\
                <td>"+item["last_time"]+"</td>\
            </tr>\
            <tr>\
                <td>脚本状态</td>\
                <td>"+item["status"]+"</td>\
            </tr>\
            <tr>\
                <td>脚本结果</td>\
                <td>"+item["result"]+"</td>\
            </tr>"
        return table_info
    def get_result_data(self, script_name):
        result_data = {}
        item = self.dao().get_result_by_script_name(script_name)[0].get_all()
        print item["data"]
        tem =self.get_script_info_by_name(script_name)
        result_data["script_name"] = tem["info"]
        result_data["last_time"] = self.tool().get_time(float(item["update_time"]))
        result_data["status"] = self.change_status_to_chinese(self.dao().get_status(script_name))
        result_data["result"] = item["data"]
        return result_data

    def start_thread(self,func,*args):
        threads = []
        t1 = threading.Thread(target=func, args=(args))
        threads.append(t1)
        lock = threading.Lock()
        lock.acquire()
        for t in threads:
            t.setDaemon(True)
            t.start()
            lock.release()

    def get_script_info_by_name(self, script_name):
        item = {}
        tem = self.tool().encode_fac(self.dao().get_script_info_by_name(script_name).get_all())
        item["name"] = tem["script_info"]
        item["info"] = tem["script_detail"]

        return item

if __name__ == '__main__':
    conn = Connctor()
    conn.get_result_data("ABtest")