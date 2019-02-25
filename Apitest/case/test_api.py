#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 16:54
# @Author  : case
import unittest
import ddt
import os
import requests
from Apitest.common import base_api
from Apitest.common import readExcel
from Apitest.common import write

# from Apitest.log.logger import logger
#获取当前路径
curpath = os.path.dirname(os.path.realpath(__file__))
#关联并查找文件
testxlsx = os.path.join(curpath, "demo-text.xlsx")
# 复制demo_api.xlsx文件到report下
report_path = os.path.join(os.path.dirname(curpath), "report")
reportxlsx = os.path.join(report_path, "result.xlsx")
#调用读取方法读取demo的文件
testdata = readExcel.ExcelUtil(testxlsx).dict_data()
# mylog = logger().getlog()
#ddt修饰方法
@ddt.ddt
# @logger('requests封装')
class Test_api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        # 如果有登录的话，就在这里先登录了
        write.copy_excel(testxlsx, reportxlsx) # 复制xlsx
    @ddt.data(*testdata)
    def test_api(self, data):
        # try:
            # 调用发送方法，传递参数
            res = base_api.send_requests(self.s, data)
            #调用写入方法
            base_api.wirte_result(res, filename=reportxlsx)
            # 读取文件中的期望结果
            check = data["checkpoint"]
            print("期望结果->：%s"%check)
            # 接口返回的结果
            res_text = res["text"]
            print("实际结果->：%s"%res_text)

            # mylog.info("期望结果->：%s"%check)
            #
            # mylog.info("实际结果->：%s"%res_text)
            # #断言
            # mylog.info("检查点->：%s,返回实际结果->:%s" % (check,res_text))
            #断言，是否存在

            self.assertIn(check, res_text, '测试失败')
if __name__ == "__main__":
    unittest.main()


