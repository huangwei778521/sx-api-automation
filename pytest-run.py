import pytest
import os


if __name__ == "__main__":
    pytest.main()
    # pytest.main(['-vs', './testcase/business/function/test_init_devices.py','--alluredir', './temp'])  #指定某些用例执行
    # 生成报告至reports目录
    os.system('allure generate ./temp -o ./reports --clean')
    # 清空temp
    os.system("rm -rf ./temp/*")
