#!/usr/bin/python
#encoding=utf8
import os
import sys
from datetime import datetime

DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5
fenc = 'utf8'


def log(level, msg):
    tm = str(datetime.now())
    if level == DEBUG:
        strout = '[%s] DEBUG:%s' % (tm, msg)
    elif level == INFO:
        strout = '[%s] INFO:%s' % (tm, msg)
    elif level == WARN:
        strout = '[%s] WARN:%s' % (tm, msg)
    elif level == ERROR:
        strout = '[%s] ERROR:%s' % (tm, msg)
    elif level == FATAL:
        strout = msg.encode(fenc)
        raise RuntimeError(msg)
    print >> sys.stderr, strout.encode(fenc)

dic_userid = {}

class KaoQin(object):
    '''
    '''
    header = u'序号 部门    姓名    员工编码    岗级    病假    事假    探亲假  有薪假  夜班天数    迟到早退    旷工    其它    加班小时(150%)  加班小时(200%)  加班小时(300%)  生产工时'
    stringfields_i2k = {2:'name', 3:'user_id'}
    intfields_i2k = {9:'yeban_days'}
    floatfiedls_i2k = {5:'bingjia',6:'shijia',7:'tanqinjia',8:'youxinjia',10:'chidaozaotui',11:'kuanggong',
            13:'overtime_hour_15',14:'overtime_hour_2', 15:'overtime_hour_3'}

    def load_line(self, line):
        items = line.split(u'\t')
        max_key = max(self.stringfields_i2k.keys() + self.intfields_i2k.keys() + self.floatfiedls_i2k.keys())
        if len(items) < max_key:
            return False
        for i in range(len(items)):
            if i in self.stringfields_i2k:
                self.__dict__[self.stringfields_i2k[i]] = items[i].strip()
            elif i in self.intfields_i2k:
                if not items[i].strip():
                    items[i] = '0'
                self.__dict__[self.intfields_i2k[i]] = int(items[i].strip())
            elif i in self.floatfiedls_i2k:
                if not items[i].strip():
                    items[i] = '0.0'
                self.__dict__[self.floatfiedls_i2k[i]] = float(items[i].strip())
        return not not self.user_id

    def key(self):
        return self.user_id.upper()

    def __init__(self):
        self.name = ''
        self.user_id = ''
        #病假, 小时
        self.bingjia = 0.0
        #事假，小时
        self.shijia = 0.0
        #探亲假, 小时
        self.tanqinjia = 0.0
        #有薪假,小时
        self.youxinjia = 0.0
        #夜班天数,天，整数
        self.yeban_days = 0
        #迟到早退，小时
        self.chidaozaotui = 0.0
        #矿工，小时，
        self.kuanggong = 0.0
        #缺勤天数, 天，整数
        self.queqin_days = 0
        #1.5倍加班小时
        self.overtime_hour_15 = 0.0
        #2倍加班小时
        self.overtime_hour_2 = 0.0
        #3倍加班小时
        self.overtime_hour_3 = 0.0

class JiXiao(object):
    '''
    '''
    stringfields_i2k = {2:'name',3:'user_id',5:'performance_level'}
    def __init__(self):
        self.name = ''
        self.user_id = ''
        self.performance_level = ''

    def load_line(self, line):
        items = line.strip().split(u'\t')
        max_key = max(self.stringfields_i2k.keys())
        if len(items) <= max_key:
            return False
        for i in range(len(items)):
            if i in self.stringfields_i2k:
                self.__dict__[self.stringfields_i2k[i]] = items[i].strip()
        return not not self.user_id

    def key(self):
        return self.user_id.upper()

