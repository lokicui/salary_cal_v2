#encoding=utf8
import os
import sys
import pdb
import re

fenc='utf8'
#绩效
#序号   部门    姓名    员工编码    岗级    绩效评定结果

#考勤
#序号   部门    姓名    员工编码    岗级    病假    事假    探亲假  有薪假  夜班天数    迟到早退    旷工    其它    加班小时(150%)  加班小时(200%)  加班小时(300%)  生产工时    备注

#final
#序号   部门名称    职员代码    职员姓名    职位名称    岗等    薪档    实发工资人数    月绩效基数  绩效评定结果    绩效评定系数    绩效调节额  岗位工资    绩效工资    回民补贴    独生子女补贴    婴幼儿补贴  工龄补贴    班长补贴    伙食标准    伙食补贴    夜餐标准    夜班个数    夜餐补助    计税补  交通补助    其他补贴    取暖费补贴  平时加班小时    公休日加班小时  法定假日加班小时    加班费  病假小时数  事假小时数  病事假扣款合计  探亲假小时数    年休假小时数    其他有薪假  旷工小时    调节扣款    缺勤天数    其它扣款    住房公积金员工  失业保险员工    养老保险员工    医疗保险员工    大额    处分扣款    租金    应发工资    免税合计    免税金额    月收入  扣除基数    应纳税所得额    个人所得税  扣款合计    实发工资

norm_dict = {}
for line in open('../conf/keymapping'):
    line = line.strip().decode(fenc)
    items = line.strip().split('\t')
    if len(items) < 2:
        continue
    normed = items[1]
    for i in range(1, len(items)):
        norm_dict[items[i]] = normed


id_re = re.compile(r'([A-z][A-z])(\d{2,4})', re.I)
def norm_id(id):
    id = trim(id)
    if id:
        try:
            m = id_re.search(id)
            prefix = m.group(1)
            suffix = int(m.group(2))
            return '%s%04d' % (prefix.upper(), suffix)
        except:
            return None
    return id


def norm_key(k):
    k = k.replace(u'（', u'(')
    k = k.replace(u'（', u'(')
    k = k.replace(u'）', u')')
    k = k.replace(u'）', u')')
    try:
        return norm_dict[trim(k)]
    except:
        return None
        pdb.set_trace()

def trim(k):
    replace_signs = {u' ':u'', u'　':u'', u'  ':u''}
    if isinstance(k, unicode):
        for i in replace_signs:
            k = k.replace(i, replace_signs[i]).strip()
    return k

