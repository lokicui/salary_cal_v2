#!/usr/bin/python
#encoding=utf8
import os
import sys
import pdb
sys.path.append('../src')
from kaoqin_jixiao import KaoQin,JiXiao
from log import log, DEBUG, INFO, WARN, ERROR, FATAL
#工时, 小时
g_work_hour = 168


class OfficalEmployee(object):
    '''
    长期工/正式工
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
        self.jixiao = JiXiao()
        self.kaoqin = KaoQin()
        self.


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


