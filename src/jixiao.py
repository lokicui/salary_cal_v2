#!/usr/bin/python
#encoding=utf8
import os
import sys
import pdb
import xlrd
import glob
from normlize import trim, norm_key, norm_id

class JiXiaoRecords(object):
    '''
    '''

    def __init__(self):
        self._i2k = {}
        self._k2i = {}
        self._id_dict = {}
        #姓名是可能重复的
        self._name_dict = {}

    def get_record(self):
        return JiXiaoRecord()

    def load(self, jixiao_dir, fenc='utf8'):
        for fname in glob.glob('%s/*.xls*' % jixiao_dir):
            data = xlrd.open_workbook(fname)
            for i in range(data.nsheets):
                table = data.sheet_by_index(0)
                head_info = table.row_values(0)
                for i in range(len(head_info)):
                    key = norm_key(head_info[i])
                    self._i2k[i] = key
                    self._k2i[key] = i
                id_idx = self._k2i[u'员工编码']
                name_idx = self._k2i[u'姓名']
                for i in range(1, table.nrows):
                    row = table.row_values(i)
                    id = norm_id(row[id_idx])
                    name = trim(row[name_idx])
                    record = self.get_record()
                    assert record.load(row, self._i2k, self._k2i)
                    self._id_dict[id] = record
                    if name not in self._name_dict:
                        self._name_dict[name] = record
                    else:
                        #发现姓名重复,则姓名再不能作为key了
                        self._name_dict[name] = None
        return True

    def __getitem__(self, k):
        if k in self._name_dict:
            return self._name_dict[k]
        if k in self._id_dict:
            return self._id_dict[k]
        return None

    def keys(self):
        return self._name_dict.keys()

class JiXiaoRecord(object):
    '''
    绩效
    '''
    def __init__(self):
        self._row = []
        self._i2k = {}
        self._k2i = {}

    def load(self, row, i2k, k2i):
        self._row = row
        self._i2k = i2k
        self._k2i = k2i
        return True

    def __getitem__(self, k):
        v = None
        if k in self._k2i:
            idx = self._k2i[k]
            v = self._row[idx]
        return trim(v)

def test(dir):
    records = JiXiaoRecords()
    records.load(dir)
    for k in records.keys():
        info = '%s:%s:%s' % (k, records[k][u'姓名'], records[k][u'员工编码'])
        print info.encode('utf8')

if __name__ == '__main__':
    test(sys.argv[1])

