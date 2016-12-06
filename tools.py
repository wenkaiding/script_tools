#!/usr/bin/python
# coding: utf-8
__author__ = 'martin'


class Tools:
    def __init__(self):
        pass

    def replace_file(self, path, ori, new, filename):
        temp = "cd {} \nsed -i 's/m{}/{}/'{}".format(path, ori, new, filename)
        return temp

    # 截取指定字符串之间的内容
    def txt_wrap_by(self, start_str, end_str, content):
        start = content.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = content.find(end_str, start)
            if end >= 0:
                return content[start:end].strip()
            else:
                return "{} is not right".format(end_str)
        else:
            return "{} is not right".format(start_str)

    def encode_fac(self, obj):
        if isinstance(obj, list):
            for item in obj:
                if isinstance(item, unicode):
                    obj[obj.index(item)] = item.encode("utf-8")
                else:
                    self.encode_fac(item)
        elif isinstance(obj, dict):
            for key, value in obj.iteritems():
                if isinstance(value, unicode):
                    obj[key] = value.encode("utf-8")
                else:
                    self.encode_fac(value)
        elif isinstance(obj, unicode):
            obj = obj.encode()
        else:
            obj = obj
        return obj
