#!/usr/bin/python
#encoding=utf8
import os
import sys
import pdb
sys.path.append('../src')
from kaoqin import KaoQinRecords
from jixiao import JiXiaoRecords
from input import InputRecords
from log import log, DEBUG, INFO, WARN, ERROR, FATAL
#工时, 小时
g_work_hour = 168

class DataLoader(object):
    '''
    '''

    def __init__(self):
        self._kaoqin = KaoQinRecords()
        self._jixiao = JiXiaoRecords()
        self._input = InputRecords()

    def load(self, kaoqin_dir, jixiao_dir, final_fname, fenc):
        self._kaoqin.load(kaoqin_dir, fenc)
        self._jixiao.load(jixiao_dir, fenc)
        self._input.load(final_fname, fenc)

    def check(self, fenc='utf8'):
        for id in self._input.ids():
            #用员工编码查的不到的用姓名查
            input_info = self._input[id]
            p = input_info[u'姓名']
            jx_info = self._jixiao[id]
            if not jx_info:
                jx_info = self._jixiao[p]
            kq_info = self._kaoqin[id]
            if not kq_info:
                kq_info = self._kaoqin[p]
            if not jx_info:
                log(WARN, 'id=%s,name=%s have no jixiao' % (id, p))
            if not kq_info:
                log(WARN, 'id=%s,name=%s have no kaoqin' % (id, p))
            jx_check_fields = [u'绩效']
            jx_check_fields = []
            kq_check_fields = [u'病假小时数', u'事假小时数', u'探亲假小时数', u'年休假小时数', u'夜班天数', u'迟到早退']
            if jx_info:
                for k in jx_check_fields:
                    if input_info[k] != jx_info[k]:
                        print p, input_info[k], jx_info[k]
            if kq_info:
                for k in kq_check_fields:
                    if not kq_info[k]:
                        continue
                    print p, input_info[k], kq_info[k]
                    continue
                    if input_info[k] != kq_info[k]:
                        print p, input_info[k], kq_info[k]

