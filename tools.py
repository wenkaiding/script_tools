#!/usr/bin/python
# coding: utf-8
import random
import string
import time

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

    def get_time(self,timeStamp):
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def get_random_string(self):
        return string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 8)).replace(' ','')

    # 建立拼音辞典
    dic_py = dict()
    f_py = open('etc/py.txt', "r")
    content_py = f_py.read()
    lines_py = content_py.split('\n')
    n = len(lines_py)
    for i in range(0, n - 1):
        word_py, mean_py = lines_py[i].split('\t', 1)  # 将line用\t进行分割，最多分一次变成两块，保存到word和mean中去
        dic_py[word_py] = mean_py
    f_py.close()

    # 建立笔画辞典
    dic_bh = dict()
    f_bh = open('etc/bh.txt', "r")
    content_bh = f_bh.read()
    lines_bh = content_bh.split('\n')
    n = len(lines_bh)
    for i in range(0, n - 1):
        word_bh, mean_bh = lines_bh[i].split('\t', 1)  # 将line用\t进行分割，最多分一次变成两块，保存到word和mean中去
        dic_bh[word_bh] = mean_bh
    f_bh.close()

    # 辞典查找函数
    def searchdict(self,dic, uchar):
        if isinstance(uchar, str):
            uchar = unicode(uchar, 'utf-8')
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            value = dic.get(uchar.encode('utf-8'))
            if value == None:
                value = '*'
        else:
            value = uchar
        return value

    # 比较单个字符
    def comp_char_PY(self,A, B):
        if A == B:
            return -1
        pyA = self.searchdict(self.dic_py, A)
        pyB = self.searchdict(self.dic_py, B)
        if pyA > pyB:
            return 1
        elif pyA < pyB:
            return 0
        else:
            bhA = eval(self.searchdict(self.dic_bh, A))
            bhB = eval(self.searchdict(self.dic_bh, B))
            if bhA > bhB:
                return 1
            elif bhA < bhB:
                return 0
            else:
                return "Are you kidding?"

    # 比较字符串
    def comp_char(self,A, B):
        charA = A["ScriptInfo"].decode("utf-8")
        charB = B["ScriptInfo"].decode("utf-8")
        n = min(len(charA), len(charB))
        i = 0
        dd = ""
        while i < n:
            dd = self.comp_char_PY(charA[i], charB[i])
            if dd == -1:
                i = i + 1
                if i == n:
                    dd = len(charA) > len(charB)
            else:
                break
        return dd

    # 排序函数
    def cnsort(self,nline):
        n = len(nline)
        for i in range(1, n):  # 插入法
            tmp = nline[i]
            j = i
            while j > 0 and self.comp_char(nline[j - 1], tmp):
                nline[j] = nline[j - 1]
                j -= 1
            nline[j] = tmp
        return nline