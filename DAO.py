#!/usr/bin/python
# coding: utf-8
import pdb

import DB
import tools as tools


class DAO:
    def __init__(self):
        self.scripts = DB.Scripts
        self.env = DB.Env
        self.session = DB.session
        self.resluts = DB.Resluts
        self.tool = tools.Tools()

    # 获取ssh连接登陆信息
    def get_connection_info(self, script_env):
        ret = self.session.query(self.env).filter(self.env.env_name == script_env).all()
        return ret[0]

    def get_script_info(self, script_name):
        ret = self.session.query(self.scripts).filter(self.scripts.script_name == script_name).all()
	return ret[0]

    def create_resluts(self, script_name, script_id, data, env, createtime, updatetime):
        resluts = self.resluts(data=data, scripts_name=script_name, scripts_id=script_id, env=env,
                               create_time=createtime, update_time=updatetime)
        ret = self.tool.encode_fac(self.session.query(self.resluts.scripts_id).all())
        tem = []
        update_info = {"data": data, "scripts_name": script_name, "env": env, "create_time": createtime,
                       "update_time": updatetime}
	for item in ret:
            tem.append(item[0])
        self.tool.encode_fac(tem)
	
	if script_id not in tem:
            self.session.add(resluts)
            self.session.commit()
        else:
            self.update_resluts(update_info, script_id)

    def update_resluts(self, resluts, script_id):
        self.session.query(self.resluts).filter(self.resluts.scripts_id == script_id).update(resluts)
        self.session.commit()

    def update_reslut_createtime(self, script_id, createtime):
        self.session.query(self.resluts).filter(self.resluts.scripts_id == script_id).update(
            {"create_time": createtime})
        self.session.commit()

    def get_all_script_info(self):
        scripts_all_data = self.session.query(self.scripts).all()
        return scripts_all_data

    def get_updatetime(self, script_name):
        updatetime = self.session.query(self.resluts.update_time).filter(self.resluts.scripts_name == script_name).all()
        print updatetime
        return updatetime

    def get_createtime(self, script_name):
        tem = self.session.query(self.resluts.create_time).filter(self.resluts.scripts_name == script_name).all()
        if isinstance(tem,list):
            if tem.__len__() == 0:
                updatetime = 0
            else:
                updatetime = tem[0][0]
        else:
            updatetime = tem

        return updatetime

    def update_script_status(self, scripname, status):
        self.session.query(self.scripts).filter(self.scripts.script_name == scripname).update({"script_status": status})
        self.session.commit()

    def get_status(self, script_name):
        status = self.session.query(self.scripts.script_status).filter(self.scripts.script_name == script_name).all()[0][0]
        return status

    def update_reslut_updatetime(self, script_id, updatetime):
        self.session.query(self.resluts).filter(self.resluts.scripts_id == script_id).update({"create_time": updatetime})
        self.session.commit()

    def get_last_script(self):
        tem = self.session.query(self.resluts).all()
        return tem

    def get_result_by_script_name(self, script_name):
        tem = self.session.query(self.resluts).filter(self.resluts.scripts_name == script_name).all()
	return tem
    def get_script_info_by_name(self, script_name):
        tem = self.session.query(self.scripts).filter(self.scripts.script_name == script_name).all()[0]
        return tem

    def get_all_script_name(self):
        """
        :return: script_name_list
        """
        name_list = self.session.query(self.scripts.script_name).all()
        return name_list

    def create_script(self, data):
        scripts = self.scripts(script_name=data["script_name"],script_info=data["script_info"],short_name=["short_name"],
                               script_content_n=data["script_content_n"],script_content_o=data["script_content_o"],
                               script_detail=data["script_detail"],script_status=data["script_status"])
        self.session.add(scripts)
        self.session.commit()
    def get_script_id(self,scrip_name):
        script_id = self.session.query(self.scripts.id).filter(self.scripts.script_name == scrip_name).all()
        return script_id

    def update_script(self, data, id):
        scripts = {
                    "script_info":data["script_info"],
                    "script_content_n":data["script_content_n"],
                    "script_content_o":data["script_content_o"],
                    "script_detail":data["script_detail"]
                    }
        print scripts
        print id
        self.session.query(self.scripts).filter(self.scripts.id == id[0][0]).update(scripts)
        self.session.commit()

    def search(self,name):
        name = self.session.query(self.scripts).filter(self.scripts.script_info.like("%"+name+"%")).all()
        return name

if __name__ == '__main__':
    dao = DAO()
    # for i in range(dao.get_all_script_info().__len__()):
    # print dao.tool.encode_fac(dao.get_all_script_info()[i].get_all())
    name =  dao.search("级")
    for item in name:
        print item.get_all()["script_content_o"]
