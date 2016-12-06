#!/usr/bin/python
# coding: utf-8
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

    def get_script_info(self, env, script_name):
        ret = self.session.query(self.scripts).filter(self.scripts.script_name == script_name,
                                                      self.scripts.script_env == env).all()
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

    def update_reslut_createtime(self, script_id, updatetime):
        self.session.query(self.resluts).filter(self.resluts.scripts_id == script_id).update(
            {"create_time": updatetime})
        self.session.commit()

    def get_all_script_info(self):
        scripts_all_data = self.session.query(self.scripts).all()
        return scripts_all_data

    def get_updatetime(self, script_name, env):
        updatetime = self.session.query(self.resluts.update_time).filter(self.resluts.scripts_name == script_name).all()
        return updatetime

    def get_createtime(self, script_name, env):
        updatetime = self.session.query(self.resluts.create_time).filter(self.resluts.scripts_name == script_name).all()
        return updatetime

    def update_script_status(self, scripname, env, status):
        self.session.query(self.scripts.script_name == scripname, self.scripts.script_env == env).update(
            {"script_status": status})
        self.session.commit()

    def get_status(self, script_name, env):
        status = self.session.query(self.scripts.script_status).filter(self.scripts.script_name == script_name, self.scripts.script_env == env).all()[0][0]
        return status


if __name__ == '__main__':
    dao = DAO()
    # for i in range(dao.get_all_script_info().__len__()):
    #     print dao.tool.encode_fac(dao.get_all_script_info()[i].get_all())
    print dao.get_status("ABtest", "Outside")[0][0]