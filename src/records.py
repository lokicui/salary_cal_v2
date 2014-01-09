#!/usr/bin/python
#encoding=utf8
import os
import sys
import pdb
import xlrd
from datetime import datetime
sys.path.append('../src')
from log import log, DEBUG, INFO, WARN, ERROR, FATAL
from normlize import trim, norm_id
from db import DBQuery
fenc='utf8'

class JixiaoRecords(BaseRecords):
    '''
    绩效
    '''
    _DB_TABLE = 'jixiao'

class KaoqinRecords(BaseRecords):
    '''
    考勤
    '''
    _DB_TABLE = 'kaoqin'

class SummaryRecords(BaseRecords):
    '''
    对应summary表
    '''
    _DB_TABLE = 'summary'


class BaseRecords(object):
    '''
    '''
    #db
    #mannual init
    _DB_TABLE = 'no_exits'
    def __init__(self):
        self._table = None
        self._k2i = {}
        self._i2k = {}
        self._id_dict = {}
        self._name_dict = {}
        self._keymapping = self.get_keymapping()

    def get_ktype(self, typestr):
        typestr = typestr.lower()
        if typestr.find('int') != -1:
            return int
        elif typestr.find('double') != -1:
            return float
        else:
            return unicode

    def get_keymapping(self):
        k2desc = {}
        desc2k = {}
        k2type = {}
        k2defaultv = {}
        sql = 'SHOW FULL COLUMNS FROM `%s`' % self._DB_TABLE
        for item in DBQuery.query(sql):
            field = item['Field']
            comment = item['Comment']
            typestr = item['Type']
            defaultv = item['Default']
            for i in comment.split('/'):
                k2desc[field] = i
                k2type[field] = self.get_ktype(typestr)
                k2defaultv[field] = defaultv
                desc2k[i] = field
        return k2desc, desc2k, k2type, k2defaultv

    def get_record(self):
        return BaseRecord()

    def load(self, excel_fname, fenc='utf8'):
        k2desc, desc2k = self._keymapping[:2]
        data = xlrd.open_workbook(excel_fname)
        #self._table = data.sheet_by_name(table_name)
        self._table = data.sheet_by_index(0)
        head_info = self._table.row_values(0)
        for i in range(len(head_info)):
            rawkey = trim(head_info[i])
            if rawkey not in desc2k:
                continue
            key = desc2k[rawkey]
            self._i2k[i] = key
            self._k2i[key] = i
        id_idx = self._k2i[u'id']
        name_idx = self._k2i[u'name']
        for i in range(1, self._table.nrows):
            row = self._table.row_values(i)
            id = norm_id(row[id_idx])
            name = trim(row[name_idx])
            record = self.get_record()
            assert record.load(row, self._i2k, self._k2i, self._keymapping)
            self._id_dict[id] = record
            if name not in self._name_dict:
                self._name_dict[name] = record
            else:
                #发现姓名重复,则姓名再不能作为key了
                self._name_dict[name] = None
        return True

    def __getitem__(self, k):
        if k in self._id_dict:
            return self._id_dict[k]
        if k in self._name_dict:
           return self._name_dict[k]
        return None

    def keys(self):
        k_ = []
        for i in self._i2k:
            k = self._i2k[i]
            k_.append(k)
        k_.append('itime')
        return k_

    def names(self):
        return self._name_dict.keys()

    def ids(self):
        return self._id_dict.keys()

    def to_db(self):
        keys = ['`%s`' % k for k in self.keys()]
        str_keys = ','.join(keys)
        sql = 'INSERT INTO `%s`(%s) VALUES (%s)' % (self._DB_TABLE, str_keys, ','.join(['%s' for i in range(len(keys))]))

        values = []
        for id in self._id_dict:
            record = self._id_dict[id]
            values.append(record.values())
            assert len(record.values()) == len(keys)
            if len(values) == 29:
                pdb.set_trace()
        DBQuery.executemany(sql, values)

class BaseRecord(object):
    '''
    输入的雇员,通常代表需要被check的员工
    每行都是一位员工的工资相关的属性
    '''

    def __init__(self):
        self._row = []
        self._i2k = {}
        self._k2i = {}
        self._keymapping = ({},{},{},{})

    def load(self, row, i2k, k2i, keymapping={}):
        self._row = row
        self._i2k = i2k
        self._k2i = k2i
        self._keymapping = keymapping
        return True

    def values(self):
        k2desc, desc2k, k2type, k2defaultv = self._keymapping
        v_ = []
        for i in self._i2k:
            k = self._i2k[i]
            try:
                v = k2type[k](self._row[i])
            except:
                v = k2defaultv[k]
                log(WARN, 'k:%s,using defaultv:%s' % (k, v))
            v_.append(v)
        itime = str(datetime.now())
        v_.append(itime)
        return v_

    def __getitem__(self, k):
        return self.get(k)

    def get(self, k):
        rawk = trim(k)
        k2desc, desc2k = self._keymapping[:2]
        k = None
        if rawk in desc2k:
            k = desc2k[rawk]
        if not k:
            return None
        if k in self._k2i:
            idx = self._k2i[k]
            return self._row[idx]
        return None


def test(excel_fname):
    employees = BaseRecords()
    employees.load(excel_fname)
    employees.to_db()
    #for k in employees.ids():
    #    pdb.set_trace()
    #    info = '%s:%s'  % (k, employees[k][u'职员姓名'])
    #    print info.encode('utf8')

if __name__ == '__main__':
    test('../data/201401/201401.xlsx')
