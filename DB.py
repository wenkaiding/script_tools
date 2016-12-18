#!/usr/bin/python
# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/scripts?charset=utf8", max_overflow=100)
Base = declarative_base()


# 创建单表
class Scripts(Base):
    # 表名
    __tablename__ = 'scripts'
    # 表字段
    id = Column(Integer, primary_key=True)  # 主键、默认自增
    script_name = Column(String(32))
    script_info = Column(String(16))
    short_name = Column(String(16))
    script_content_n = Column(String(254))
    script_content_o = Column(String(254))
    script_detail = Column(String(32))
    script_status = Column(Integer)

    def get_all(self):
        return {"id": self.id,
                "script_content_o": self.script_content_o,
                "script_content_n": self.script_content_n,
                "script_info": self.script_info,
                "script_name": self.script_name,
                "script_status": self.script_status,
                "short_name": self.short_name,
                "script_detail": self.script_detail
                }

# 创建单表
class Env(Base):
    # 表名
    __tablename__ = 'env'
    # 表字段
    id = Column(Integer, primary_key=True)  # 主键、默认自增
    env_name = Column(String(32))
    env_info = Column(String(16))
    env_hosts = Column(String(16))
    env_username = Column(String(32))
    env_password = Column(String(32))
    env_port = Column(String(32))


# 创建单表
class Resluts(Base):
    # 表名
    __tablename__ = 'resluts'
    # 表字段
    id = Column(Integer, primary_key=True)  # 主键、默认自增
    data = Column(String(254))
    env = Column(String(32))
    scripts_name = Column(String(16))
    scripts_id = Column(Integer)
    update_time = Column(String(32))
    create_time = Column(String(32))
    def get_all(self):
        return {
            "id":self.id,
            "data":self.data,
            "env":self.env,
            "scripts_name":self.scripts_name,
            "update_time":self.update_time,
            "create_time":self.create_time
        }

def init_db():
    # 创建表
    Base.metadata.create_all(engine)


def drop_db():
    # 删除表
    Base.metadata.drop_all(engine)


Session = sessionmaker(bind=engine)  # 指定引擎
session = Session()
