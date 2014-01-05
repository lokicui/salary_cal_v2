#!/usr/bin/python
#encoding=utf8
import os
import sys
import pdb
sys.path.append('../src')
from datetime import datetime
from kaoqin_jixiao import KaoQin,JiXiao
#工时, 小时
g_work_hour = 168

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

class DataLoader(object):
    '''
    data loader
    '''
    header_k2i = {}
    header_i2k = {}
    def __init__(self):
        self.employee_dict = {}
    #init at load_header
    #key to index
    def load_file(self, final_fname, kaoqin_fname, jixiao_fname):
        self.load_kaoqin(kaoqin_fname)
        self.load_jixiao(jixiao_fname)
        self.load_final(final_fname)

    def load_kaoqin(self, kaoqin_fname):
        lineno = 0
        for line in open(kaoqin_fname):
            lineno += 1
            line = line.decode(fenc, 'ignore')
            kaoqin = KaoQin()
            if not line.strip() or not kaoqin.load_line(line.strip()):
                log(WARN, 'kaoqin load failed, line[%s]' % line.strip())
                continue
            self.employee_dict.setdefault(kaoqin.key(), Employee())
            self.employee_dict[kaoqin.key()].kaoqin = kaoqin
            self.employee_dict[kaoqin.key()].kaoqin_rawline = line.strip()
            self.employee_dict[kaoqin.key()].kaoqin_lineno = lineno

    def load_jixiao(self, jixiao_fname):
        lineno = 0
        for line in open(jixiao_fname):
            lineno += 1
            line = line.decode(fenc)
            jixiao = JiXiao()
            if not line.strip() or not jixiao.load_line(line.strip()):
                log(WARN, 'jixiao load failed, line[%s]' % line.strip())
                continue
            self.employee_dict.setdefault(jixiao.key(), Employee())
            self.employee_dict[jixiao.key()].jixiao = jixiao
            self.employee_dict[jixiao.key()].jixiao_rawline = line.strip()
            self.employee_dict[jixiao.key()].jixiao_lineno = lineno

    def load_final(self, final_fname):
        lineno = 0
        for line in open(final_fname):
            lineno += 1
            line = line.decode(fenc, 'ignore')
            if lineno == 1:
                self.load_header(line)
            else:
                em = Employee()
                if not line.strip() or not em.load_line(line.strip(), self.header_i2k, lineno):
                    log(ERROR, 'load_line failed:%s' % line)
                self.employee_dict.setdefault(em.key(), Employee())
                self.employee_dict[em.key()].load_line(line, self.header_i2k, lineno)

    def load_header(self, line):
        items = line.split('\t')
        for i in range(0, len(items)):
            self.header_k2i[items[i]] = i
            self.header_i2k[i] = items[i]

    def check(self):
        for k,v in self.employee_dict.items():
            #if k == 'LR0015':
            #    pdb.set_trace()
            v.check()

class Employee(object):
    '''
    雇员
    '''
   #mannual init
    floatfields_i2k = {9:'post_wage', 12:'input_performance_ratio', 14:'jishui_allowance',16:'input_bingjia',17:'input_shijia',19:'input_tanqinjia',
            20:'input_youxinjia',23:'input_chidaozaotui',24:'input_kuanggong',26:'input_other_debit',27:'input_overtime_hour_15',
            28:'input_overtime_hour_2', 29:'input_overtime_hour_3',30:'input_overtime_wage',33:'huimin_allowance',
            38:'huoshi_allowance',39:'zhufang_qiye',40:'shiye_yuangong',41:'yanglao_yuangong',42:'yiliao_yuangong',
            43:'yanglao_qiye',44:'yiliao_qiye',45:'shiye_qiye',46:'gongshang_qiye',47:'shengyu_qiye',48:'input_qiye_baoxian',
            50:'other_allowance',51:'qunuan_allowance',52:'input_labor_cost'}
    intfields_i2k = {0:'seq',7:'xindang',8:'post_wage_base',10:'month_performance_base',13:'input_performance_wage',
            21:'input_yeban_days',25:'input_queqin_days',31:'service_allowance',32:'squard_allowance',
            34:'only_child_allowance',35:'child_allowance',36:'traffic_allowance',37:'yuecanbu',
            49:'input_guanlifei'}
    stringfields_i2k = {1:'department', 3:'name', 4:'user_id',6:'level',11:'input_performance_level',15:'staffing_company'}
    def __init__(self):
        self.dic = {}
        self.kaoqin_rawline = ''
        self.jixiao_rawline = ''
        self.rawline = ''
        self.lineno = 0
        self.kaoqin_lineno = 0
        self.jixiao_lineno = 0
        # 序号
        self.seq = 0
        self.name = ''
        #员工编码
        self.user_id = ''
        #部门
        self.department = ''
        #职位
        self.position = ''
        #职级
        self.level = ''
        #派遣公司
        self.staffing_company = ''
        #薪档, 整数
        self.xindang = 0
        #岗位工资基数, 整数
        self.post_wage_base = 0
        #月绩效基数 整数
        self.month_performance_base = 0
        #岗位工资
        self.post_wage = 0.0
        #计税补
        self.jishui_allowance = 0.0
        #考勤
        self.kaoqin = KaoQin()
        #绩效
        self.jixiao = JiXiao()

        #工龄补贴
        self.service_allowance = 0
        #班长补贴
        self.squard_allowance = 0
        #回民补贴
        self.huimin_allowance = 0.0
        #独生子女补贴
        self.only_child_allowance = 0
        #婴幼儿补贴
        self.child_allowance = 0
        #交通补贴
        self.traffic_allowance = 0
        #月餐补
        self.yuecanbu = 0
        #住房公积金企业
        self.zhufang_qiye = 0.0
        #失业保险员工
        self.shiye_yuangong = 0.0
        #养老保险员工
        self.yanglao_yuangong = 0.0
        #医疗保险员工
        self.yiliao_yuangong = 0.0
        #养老保险企业
        self.yanglao_qiye = 0.0
        #医疗保险企业
        self.yiliao_qiye = 0.0
        #失业保险企业
        self.shiye_qiye = 0.0
        #工伤保险企业
        self.gongshang_qiye = 0.0
        #生育保险企业
        self.shengyu_qiye = 0.0
        #管理费
        self.guanlifei = 0
        #其他补贴
        self.other_allowance = 0.0
        # 取暖费补贴
        self.qunuan_allowance = 0.0
        # 补发合计
        self.bufa_heji = 0.0


        ###########################################
        #计算得到, 不能变换计算顺序
        ###########################################
        #绩效系数
        self.performance_ratio = 0.0
        #绩效工资
        self.performance_wage = 0.0
        #病事假扣款
        self.bingshijia_debit = 0.0
        #夜餐补贴 = 夜班天数 *12
        self.yecan_allowance = 0.0
        #其他扣款
        self.other_debit = 0.0
        #加班费
        self.overtime_wage = 0.0
        #伙食补贴
        self.huoshi_allowance = 0.0
        #企业保险
        self.qiye_baoxian = 0.0
        #人工成本合计
        self.labor_cost = 0.0

        #################################################################
        # 需要核对项目
        #################################################################
        self.input_labor_cost = 0.0
        self.input_other_debit = 0.0
        self.input_qiye_baoxian = 0.0
        self.input_guanlifei = 0.0
        self.input_performance_wage = 0.0
        self.input_performance_ratio = 0.0
        #########考勤表
        #病假, 小时
        self.input_bingjia = 0.0
        #事假，小时
        self.input_shijia = 0.0
        #探亲假, 小时
        self.input_tanqinjia = 0.0
        #有薪假,小时
        self.input_youxinjia = 0.0
        #夜班天数,天，整数
        self.input_yeban_days = 0
        #迟到早退，小时
        self.input_chidaozaotui = 0.0
        #矿工，小时，
        self.input_kuanggong = 0.0
        #缺勤天数, 天，整数
        self.input_queqin_days = 0
        #1.5倍加班小时
        self.input_overtime_hour_15 = 0.0
        #2倍加班小时
        self.input_overtime_hour_2 = 0.0
        #3倍加班小时
        self.input_overtime_hour_3 = 0.0
        ###### 绩效表
        #绩效等级
        self.input_performance_level = ''

    def key(self):
        return self.user_id.upper()

    def check(self, eps=1e-9):
        #debug = True
        debug = False
        if not abs(self.input_bingjia - self.kaoqin.bingjia) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]病假[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_bingjia, self.kaoqin.bingjia))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))

            return False
        if not abs(self.input_shijia - self.kaoqin.shijia) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]事假[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_shijia, self.kaoqin.shijia))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #探亲假, 小时
        if not abs(self.input_tanqinjia - self.kaoqin.tanqinjia) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]探亲假[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_tanqinjia, self.kaoqin.tanqinjia))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #有薪假,小时
        if not abs(self.input_youxinjia - self.kaoqin.youxinjia) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]有薪假[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_youxinjia, self.kaoqin.youxinjia))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #夜班天数,天，整数
        if not self.input_yeban_days == self.kaoqin.yeban_days:
            log(ERROR, u'员工编码[%s]姓名[%s]夜班天数[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_yeban_days, self.kaoqin.yeban_days))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #迟到早退，小时
        if not abs(self.input_chidaozaotui - self.kaoqin.chidaozaotui) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]迟到早退[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_chidaozaotui, self.kaoqin.chidaozaotui))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #矿工，小时，
        if not abs(self.input_kuanggong - self.kaoqin.kuanggong) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]矿工[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_kuanggong, self.kaoqin.kuanggong))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #缺勤天数, 天，整数
        if not self.input_queqin_days == self.kaoqin.queqin_days:
            log(ERROR, u'员工编码[%s]姓名[%s]缺勤天数[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_queqin_days, self.kaoqin.queqin_days))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #1.5倍加班小时
        if not abs(self.input_overtime_hour_15 - self.kaoqin.overtime_hour_15) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]1.5倍加班小时数[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_overtime_hour_15, self.kaoqin.overtime_hour_15))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #2倍加班小时
        if not abs(self.input_overtime_hour_2 - self.kaoqin.overtime_hour_2) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]2倍加班小时数[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_overtime_hour_2, self.kaoqin.overtime_hour_2))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        #3倍加班小时
        if not abs(self.input_overtime_hour_3 - self.kaoqin.overtime_hour_3) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]3倍加班小时数[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_overtime_hour_3, self.kaoqin.overtime_hour_3))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False

        if not abs(self.input_performance_wage - self.performance_wage) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]绩效工资[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_performance_wage, self.performance_wage))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        if not abs(self.input_other_debit - self.other_debit) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]其他扣款[%s->%s]不匹配' % (self.user_id, self.name,
                self.input_other_debit, self.other_debit))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        elif not abs(self.input_qiye_baoxian - self.qiye_baoxian) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]企业保险[%s->%s]不匹配' % (self.user_id, self.name,
                self.input_qiye_baoxian, self.qiye_baoxian))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        elif not abs(self.input_guanlifei - self.guanlifei) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]派遣公司[%s]管理费[%s->%s]不匹配' % (self.user_id, self.name,
                self.staffing_company, self.input_guanlifei, self.guanlifei))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        elif not abs(self.input_labor_cost - self.labor_cost) < eps:
            log(ERROR, u'员工编码[%s]姓名[%s]人工成本[%s->%s]不匹配' % (self.user_id,
                self.name, self.input_labor_cost, self.labor_cost))
            log(ERROR, u'员工编码[%s]姓名[%s] [%s]' % (self.user_id,
                self.name, self.__dict__))
            if debug:
                log(ERROR, 'lineno=%d,line=%s' % (self.lineno, self.rawline))
                log(ERROR, 'kaoqin lineno=%d,line=%s' % (self.kaoqin_lineno, self.kaoqin_rawline))
                log(ERROR, 'jixiao lineno=%d,line=%s' % (self.jixiao_lineno, self.jixiao_rawline))
            return False
        return abs(self.input_other_debit - self.other_debit) < eps and\
               abs(self.input_labor_cost - self.labor_cost) < eps and\
               abs(self.input_qiye_baoxian - self.qiye_baoxian) < eps and\
               abs(self.input_guanlifei - self.guanlifei) < eps

    def load_line(self, line, i2k, lineno=0):
        line = line.strip()
        items = line.split('\t')
        if len(items) < 3:
            return False
        self.rawline = line
        self.lineno = lineno
        for i in range(len(items)):
            if i >= len(i2k):
                break
            self.dic[i2k[i]] = items[i]
            if i in self.floatfields_i2k:
                try:
                    if items[i] == '':
                        items[i] = '0.0'
                    self.__dict__[self.floatfields_i2k[i]] = float(items[i])
                except:
                    log(WARN, u'员工编码[%s] 列[%s] 对应的值[%s]非法' % (self.user_id, i2k[i], items[i]))
                    return False
            elif i in self.intfields_i2k:
                try:
                    if items[i] == '':
                        items[i] = '0'
                    self.__dict__[self.intfields_i2k[i]] = int(items[i])
                except:
                    log(WARN, u'员工编码[%s] 列[%s] 对应的值[%s]非法' % (self.user_id, i2k[i], items[i]))
                    return False
            elif i in self.stringfields_i2k:
                try:
                    self.__dict__[self.stringfields_i2k[i]] = items[i]
                except:
                    log(WARN, u'员工编码[%s] 列[%s] 对应的值[%s]非法' % (self.user_id, i2k[i], items[i]))
                    return False
        ###########################################
        #计算得到, 不能变换计算顺序
        ###########################################
        #计算派遣公司管理费
        self.guanlifei = self.get_guanlifei()
        #绩效系数
        self.performance_ratio = self.get_performance_ratio()
        #绩效工资, 四舍五入
        self.performance_wage = int(self.get_performance_wage() + 0.5)
        #病事假扣款
        self.bingshijia_debit = int(self.get_bingshijia_debit() + 0.5)
        #夜餐补贴 = 夜班天数 *12
        self.yecan_allowance = self.get_yecan_allowance()
        #其他扣款
        self.other_debit = int(self.get_other_debit() + 0.5)
        #加班费, 四舍五入
        self.overtime_wage = int(self.get_overtime_wage() + 0.5)
        #伙食补贴
        self.huoshi_allowance = int(self.get_huoshi_allowance() + 0.5)
        if self.huoshi_allowance < 0:
            self.huoshi_allowance = 0
        #企业保险
        self.qiye_baoxian = self.get_qiye_baoxian()
        #人工成本合计
        self.labor_cost = self.get_labor_cost()
        return True

    def get_guanlifei(self):
        dic = {u'融德':85, u'蓝天':60, u'others':70}
        for k,v in dic.items():
            if self.staffing_company.find(k) != -1:
                return v
        return dic[u'others']

    def get_labor_cost(self):
        return self.qunuan_allowance + self.other_allowance + self.guanlifei + self.qiye_baoxian +\
                self.huoshi_allowance + self.child_allowance + self.only_child_allowance + \
                self.huimin_allowance + self.squard_allowance + self.service_allowance + \
                self.overtime_wage - self.other_debit + self.yecan_allowance - self.bingshijia_debit + \
                self.jishui_allowance + self.performance_wage + self.post_wage + self.traffic_allowance + \
                self.bufa_heji

    def get_qiye_baoxian(self):
        return self.zhufang_qiye + self.yanglao_qiye + self.yiliao_qiye + self.shiye_qiye + \
                self.gongshang_qiye  + self.shengyu_qiye

    def get_huoshi_allowance(self):
        global g_work_hour
        return self.yuecanbu - self.yuecanbu * 1.0 / g_work_hour * \
                (self.kaoqin.bingjia + self.kaoqin.shijia + self.kaoqin.tanqinjia + self.kaoqin.kuanggong) -\
                self.yuecanbu * 1.0 / 30 * self.kaoqin.queqin_days

    def get_overtime_wage(self):
        return (self.post_wage + self.month_performance_base) / 21.75 / 8 * \
                (1.5 * self.kaoqin.overtime_hour_15 + 2 * self.kaoqin.overtime_hour_2 + 3 * self.kaoqin.overtime_hour_3)

    def get_other_debit(self):
        return self.post_wage / 21.75 / 8 / 2 * self.kaoqin.tanqinjia + \
                (self.post_wage + self.performance_wage) / 21.75 / 8 * self.kaoqin.kuanggong + \
                self.post_wage / 30  * self.kaoqin.queqin_days

    def get_performance_ratio(self):
        dic = {'A':1.4, 'B':1.2, 'C':1, 'D':0.8, 'E':0.6}
        if self.jixiao.performance_level in dic:
            return dic[self.jixiao.performance_level]
        return self.input_performance_ratio

    def get_performance_wage(self):
        global g_work_hour
        return self.month_performance_base * 1.0 / g_work_hour * self.kaoqin.youxinjia + \
                self.month_performance_base * 1.0 / g_work_hour * ( g_work_hour - self.kaoqin.youxinjia) * self.performance_ratio

    def get_bingshijia_debit(self):
        return self.post_wage / 21.75 / 8 * self.kaoqin.bingjia + \
                (self.post_wage + self.performance_wage) / 21.75 / 8 * self.kaoqin.shijia

    def get_yecan_allowance(self):
        return self.kaoqin.yeban_days * 12


def test(fname,kaoqin_file, jixiao_file):
    dl = DataLoader()
    dl.load_file(fname, kaoqin_file, jixiao_file)
    dl.check()

if __name__ == '__main__':
    test(sys.argv[1], sys.argv[2], sys.argv[3])
