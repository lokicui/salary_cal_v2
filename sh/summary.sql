-- phpMyAdmin SQL Dump
-- version 4.1.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2014-01-09 23:08:39
-- 服务器版本： 5.5.34-0ubuntu0.12.04.1
-- PHP Version: 5.3.10-1ubuntu3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `salary`
--

-- --------------------------------------------------------

--
-- 表的结构 `summary`
--

CREATE TABLE IF NOT EXISTS `summary` (
  `id` varchar(8) COLLATE utf8_bin NOT NULL COMMENT '职员代码',
  `name` varchar(16) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '员工姓名/职员姓名',
  `department` varchar(32) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '部门',
  `position` varchar(8) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '职位',
  `level` varchar(8) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '职级',
  `bingjia_hour` double NOT NULL DEFAULT '0' COMMENT '病假小时数',
  `shijia_hour` double NOT NULL DEFAULT '0' COMMENT '事假小时数',
  `tanqinjia_hour` double NOT NULL DEFAULT '0' COMMENT '探亲假小时数',
  `nianxiujia_hour` double NOT NULL DEFAULT '0' COMMENT '年休假小时数',
  `kuangong_hour` double NOT NULL DEFAULT '0' COMMENT '旷工小时数',
  `overtime_hour_15` double NOT NULL DEFAULT '0' COMMENT '1.5倍加班小时数',
  `overtime_hour_2` double NOT NULL DEFAULT '0' COMMENT '2倍加班小时数',
  `overtime_hour_3` double NOT NULL DEFAULT '0' COMMENT '3倍加班小时数',
  `staffing_company` varchar(16) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '派遣公司',
  `xindang` int(11) NOT NULL DEFAULT '0' COMMENT '薪档',
  `absence_days` double NOT NULL DEFAULT '0' COMMENT '缺勤天数',
  `large` double NOT NULL DEFAULT '0' COMMENT '大额',
  `punishment_debit` double NOT NULL DEFAULT '0' COMMENT '处分扣款',
  `rent` double NOT NULL DEFAULT '0' COMMENT '租金',
  `wages_should` double NOT NULL DEFAULT '0' COMMENT '应发工资',
  `total_exemption` double NOT NULL DEFAULT '0' COMMENT '免税合计',
  `post_wage_base` double NOT NULL DEFAULT '0' COMMENT '岗位工资基数',
  `yeban_days` double NOT NULL DEFAULT '0' COMMENT '夜班天数',
  `reduction_base` double NOT NULL DEFAULT '0' COMMENT '扣除基数',
  `month_performance_base` int(11) NOT NULL DEFAULT '0' COMMENT '月绩效基数 整数',
  `post_wage` double NOT NULL DEFAULT '0' COMMENT '岗位工资',
  `jishui_allowance` double NOT NULL DEFAULT '0' COMMENT '计税补',
  `service_allowance` double NOT NULL DEFAULT '0' COMMENT '工龄补贴',
  `squard_allowance` double NOT NULL DEFAULT '0' COMMENT '班长补贴',
  `huimin_allowance` double NOT NULL DEFAULT '0' COMMENT '回民补贴',
  `only_child_allowance` double NOT NULL DEFAULT '0' COMMENT '独生子女补贴',
  `child_allowance` double NOT NULL DEFAULT '0' COMMENT '婴幼儿补贴',
  `traffic_allowance` double NOT NULL DEFAULT '0' COMMENT '交通补贴',
  `yuecanbu` double NOT NULL DEFAULT '0' COMMENT '月餐补',
  `zhufang_qiye` double NOT NULL DEFAULT '0' COMMENT '住房公积金企业',
  `shiye_yuangong` double NOT NULL DEFAULT '0' COMMENT '失业保险员工',
  `yanglao_yuangong` double NOT NULL DEFAULT '0' COMMENT '养老保险员工',
  `yiliao_yuangong` double NOT NULL DEFAULT '0' COMMENT '医疗保险员工',
  `housing_fund_yuangong` double NOT NULL DEFAULT '0' COMMENT '住房公积金员工',
  `yanglao_qiye` double NOT NULL DEFAULT '0' COMMENT '养老保险企业',
  `yiliao_qiye` double NOT NULL DEFAULT '0' COMMENT '医疗保险企业',
  `shiye_qiye` double NOT NULL DEFAULT '0' COMMENT '失业保险企业',
  `gongshang_qiye` double NOT NULL DEFAULT '0' COMMENT '工伤保险企业',
  `shengyu_qiye` double NOT NULL DEFAULT '0' COMMENT '生育保险企业',
  `guanlifei` double NOT NULL DEFAULT '0' COMMENT '管理费',
  `other_allowance` double NOT NULL DEFAULT '0' COMMENT '其他补贴',
  `qunuan_allowance` double NOT NULL DEFAULT '0' COMMENT '取暖费补贴',
  `bufa_heji` double NOT NULL DEFAULT '0' COMMENT '补发合计',
  `performance` varchar(8) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '绩效评定结果',
  `performance_adjustment` double NOT NULL DEFAULT '0' COMMENT '绩效调节额',
  `performance_ratio` double NOT NULL DEFAULT '0' COMMENT '绩效系数',
  `performance_wage` double NOT NULL DEFAULT '0' COMMENT '绩效工资',
  `bingshijia_debit` double NOT NULL DEFAULT '0' COMMENT '病事假扣款',
  `yecan_allowance` double NOT NULL DEFAULT '0' COMMENT '夜餐补贴',
  `adjust_debit` double NOT NULL DEFAULT '0' COMMENT '调节扣款',
  `other_debit` double NOT NULL DEFAULT '0' COMMENT '其他扣款',
  `overtime_wage` double NOT NULL DEFAULT '0' COMMENT '加班费',
  `huoshi_allowance` double NOT NULL DEFAULT '0' COMMENT '伙食补贴',
  `food_standards` double NOT NULL DEFAULT '0' COMMENT '伙食标准',
  `supper_standard` double NOT NULL DEFAULT '0' COMMENT '夜餐标准',
  `qiye_baoxian` double NOT NULL DEFAULT '0' COMMENT '企业保险',
  `tax_income` double NOT NULL DEFAULT '0' COMMENT '应纳税所得额',
  `tax` double NOT NULL DEFAULT '0' COMMENT '个人所得税',
  `total_deductions` double NOT NULL DEFAULT '0' COMMENT '扣款合计',
  `income` double NOT NULL DEFAULT '0' COMMENT '实发工资',
  `labor_cost` double NOT NULL DEFAULT '0' COMMENT '人工成本合计',
  `itime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '插入时间',
  `utime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='汇总表';

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
