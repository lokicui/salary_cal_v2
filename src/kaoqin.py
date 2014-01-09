#!/usr/bin/python
#encoding=utf8
import os
import sys
import pdb
import xlrd
import glob
from normlize import trim, norm_key, norm_id
from log import log, DEBUG, INFO, WARN, ERROR, FATAL

class KaoQinRecords(object):
    '''
    所有人的考勤
    '''

    def __init__(self):
        self._id_dict = {}
        self._name_dict = {}
        self._i2k = {}
        self._k2i = {}
        self._id_dict = {}
        self._name_dict = {}

    def get_record(self):
        return KaoQinRecord()

    def load(self, kaoqin_dir, fenc='utf8'):
        for fname in glob.glob('%s/*.xls*' % kaoqin_dir):
            filename = os.path.split(fname)[-1].decode(fenc)
            data = xlrd.open_workbook(fname)
            #考勤excel只允许出现一张table
            for i in range(1):
                table = data.sheet_by_index(i)
                start = 0
                end = table.nrows
                for i in range(0, table.nrows):
                    row = table.row_values(i)
                    if trim(row[0]) == u'序号' and start == 0:
                        start = i
                    if start and trim(row[0]) == u'合计':
                        end = i
                head_info = table.row_values(start)
                for i in range(len(head_info)):
                    if not head_info[i]:
                        break
                    key = norm_key(head_info[i])
                    if not key:
                        log(ERROR, 'fname:%s key=%s head_info ERROR' % (filename, head_info[i]))
                    self._i2k[i] = key
                    self._k2i[key] = i
                id_idx = self._k2i[u'员工编码']
                name_idx = self._k2i[u'姓名']
                for i in range(start + 1, end):
                    row = table.row_values(i)
                    id = norm_id(row[id_idx])
                    name = trim(row[name_idx])
                    if not id and not name:
                        break
                    if isinstance(id, int) or isinstance(id, float):
                        continue
                    if isinstance(name, float) or isinstance(name, int):
                        continue
                    if not id or not name:
                        log(WARN, 'fname=%s,lineno=%d, id=%s,name=%s' % (filename,i,row[id_idx], row[name_idx]))
                        continue
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

class KaoQinRecord(object):
    '''
    考勤
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
    records = KaoQinRecords()
    records.load(dir)
    for k in records.keys():
        info = '%s:%s:%s' % (k, records[k][u'姓名'], records[k][u'员工编码'])
        #print info.encode('utf8')

if __name__ == '__main__':
    test(sys.argv[1])

