-- phpMyAdmin SQL Dump
-- version 4.1.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2014-01-10 00:38:07
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
-- 表的结构 `kaoqin`
--

CREATE TABLE IF NOT EXISTS `kaoqin` (
  `id` varchar(8) COLLATE utf8_bin NOT NULL,
  `name` varchar(16) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '员工姓名',
  `department` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '部门',
  `bingjia` double NOT NULL DEFAULT '0' COMMENT '病假小时数',
  `shijia` double DEFAULT '0' COMMENT '事假小时数',
  `tanqinjia` double NOT NULL DEFAULT '0' COMMENT '探亲假小时数',
  `youxinjia` double NOT NULL DEFAULT '0' COMMENT '有薪假小时数',
  `yeban_days` double NOT NULL DEFAULT '0' COMMENT '夜班天数',
  `chidaozaotui` double NOT NULL DEFAULT '0' COMMENT '迟到早退小时数',
  `kuanggong` double NOT NULL DEFAULT '0' COMMENT '旷工小时数',
  `queqin_days` double NOT NULL DEFAULT '0' COMMENT '缺勤天数',
  `overtime_hour_15` double NOT NULL DEFAULT '0' COMMENT '1.5倍加班小时数',
  `overtime_hour_2` double NOT NULL DEFAULT '0' COMMENT '2倍加班小时数',
  `overtime_hour_3` double NOT NULL DEFAULT '0' COMMENT '3倍加班小时数',
  `itime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '插入时间',
  `utime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='考勤';

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
