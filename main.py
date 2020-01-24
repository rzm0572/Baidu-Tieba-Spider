# -*- coding: utf-8 -*-
# Author: rzm
# Create time: 2020/01/23 22:01

from tiebaSpider import TiebaSpider

code = input("请输入帖子编号：")
add_info_inp = input("是否添加信息(y/[n])：")
only_lz_inp = input("是否只看楼主([y]/n)：")
path = input("请输入存储位置：")

add_info = False
only_lz = True

if add_info_inp is not None and add_info_inp == 'y':
    add_info = True

if only_lz_inp is not None and only_lz_inp == 'n':
    only_lz = False

try:
    contents = TiebaSpider(code, path, add_info, only_lz)
except Exception:
    print("ERROR!")
finally:
    input("按任意键退出...")
