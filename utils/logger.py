import os
import logging
import os.path
import time


def basic_log(module, file_name):
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        filename=f"{root_path}/logs/{module}/{file_name}",
        filemode="a",
    )


def logger_handler(log_path=None, log_file_path=None):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    if log_file_path:
        logfile = log_file_path
    else:
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        logfile = log_path + rq + ".log"
    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    formatter = logging.Formatter()
    fh.setFormatter(formatter)
    # 第四步，将log添加到handler里面

    log.addHandler(fh)
    return log
