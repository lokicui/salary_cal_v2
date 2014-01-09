-- phpMyAdmin SQL Dump
-- version 4.1.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2014-01-10 00:38:31
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
-- 表的结构 `jixiao`
--

CREATE TABLE IF NOT EXISTS `jixiao` (
  `id` varchar(8) COLLATE utf8_bin NOT NULL,
  `name` varchar(16) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '员工姓名',
  `performance_level` varchar(4) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '绩效等级',
  `itime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '插入时间',
  `utime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='绩效';

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
