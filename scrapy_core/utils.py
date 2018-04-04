#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/25 19:33
# @Author  : hyang
# @Site    : 
# @File    : utils.py
# @Software: PyCharm


# 打印信息
def print_log(msg, log_type="info"):
    if log_type == 'info':
        print("\033[32;1m%s\033[0m" %msg)
    elif log_type == 'error':
        print("\033[31;1m%s\033[0m" %msg)


# 输入信息
def input_log(msg, log_type="info"):
    if log_type == 'info':
        return input("\033[32;1m%s\033[0m" % msg)
    elif log_type == 'error':
        return input("\033[31;1m%s\033[0m" % msg)

