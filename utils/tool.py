import argparse
import asyncio
import base64
import datetime
import math
import os
import subprocess
import time
from functools import wraps
from pathlib import Path

import aiohttp


def get_item_by_key(obj, key, result=None):
    if isinstance(obj, dict):
        for k in obj:
            if key == k:
                if isinstance(result, list):
                    if isinstance(obj[k], list):
                        result.extend(obj[k])
                    else:
                        result.append(obj[k])
                elif result is None:
                    result = obj[k]
                else:
                    tmp = [result]
                    result = tmp
                    result.append(obj[k])
            else:
                if isinstance(obj[k], dict) or isinstance(obj[k], list):
                    result = get_item_by_key(obj[k], key, result)
    elif isinstance(obj, list):
        for i in obj:
            if isinstance(i, dict) or isinstance(i, list):
                result = get_item_by_key(i, key, result)
    return result[0] if isinstance(result, list) and len(result) == 1 else result


def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True)
    stdout, sdtin = p.communicate()
    stdout = stdout.strip()
    ls = [i.split(' ')[-1][:-1] for i in stdout.split('\n') if 'G' or 'B' in i]
    return set(ls)


def time_delta(**kwargs):
    delta_time = datetime.datetime.now() + datetime.timedelta(**kwargs)
    delta_time = delta_time.strftime('%Y-%m-%d %H:%M:%S')
    return delta_time


def network_disconnect(ssh, eth='eth0', i_num=10, c_time=5, i_time=5):
    """
        网络间歇性闪断(默认闪断持续3秒间隔5秒模拟5次)
    :param ssh: ssh连接对象
    :param eth: 网卡，默认eth100
    :param i_num: 闪断次数
    :param c_time: 中断持续时间
    :param i_time: 间隔时间
    :return:
    """
    cmd_network = 'ifdown %s;sleep %s;ifup %s;sleep %s;' % (eth, c_time, eth, i_time) * i_num
    ssh.run('echo "%s" >> tmp.sh && chmod +x tmp.sh && ./tmp.sh && rm -f tmp.sh' % cmd_network)
    return True


def get_pod_info(ssh, pods_prefix_list):
    pod_list = []
    for pod_prefix in pods_prefix_list:
        pod_info = ssh.run_cmd('kubectl get pod --all-namespaces -o wide | grep %s' % pod_prefix)
        pod = [filter(None, elem.split(' ')) for elem in pod_info]
        pod_list.append(pod[0])
    return pod_list


def get_pod_pid(ssh, pod_name, namespace='default'):
    """
        获取pod对应的进程id
    :param ssh: ssh连接对象
    :param pod_name: pod的名称
    :param namespace: pod所在的名称空间
    :return:
    """
    return ssh.run_cmd('kubectl describe pods --namespace=%s %s '
                       '| grep "Container ID" | cut -d \\/ -f 3' % (namespace, pod_name))


def kill_pod(ssh, pid):
    """
        杀掉pod对应的进程
    :param ssh: ssh连接对象
    :param pid: 进程id
    :return:
    """
    for p in pid:
        ssh.run_cmd('docker inspect -f "{{.State.Pid}}" %s | xargs kill -9' % p)


def get_pod_not_running(ssh, _filter=None):
    """
        获取被测机器的未正常运行pod的信息
    :param ssh: ssh连接对象
    :param _filter:
    :return: < [pod所在的名称空间, pod名称, 运行的个数/pod里容器个数, 状态, 重启次数, 运行时长, 集群ip, 所在主机名] : list>
    """
    pod_info = [pod.split() for pod in ssh.run_cmd('kubectl get pod --all-namespaces | grep -v Running')[1:]]

    err_pod = []
    for elem in pod_info:
        if elem[1] in _filter:
            err_pod.append(elem[1])
    return err_pod


def shutdown(ssh):
    """
        立刻关闭被测机器
    :param ssh: ssh连接对象
    :return:
    """
    ssh.run_cmd('sudo shutdown -h now')
    return True


def reboot(ssh):
    """
        重启被测机器
    :param ssh:
    :return:
    """
    ssh.run_cmd('sudo reboot')
    return True


def ipmitool(bmc_ip, ipmi_type, user='root', password='1pMi@#$%'):
    """
        bmc复位机器
    :param bmc_ip:
    :param user:
    :param password:
    :return:
    """
    cmd = f"ipmitool -I lanplus -H {bmc_ip} -U {user} -P {password} chassis power {ipmi_type}"
    with os.popen(cmd) as fr:
        msg = fr.readline().strip("\n")

    if ipmi_type == "reset":
        if msg == 'Chassis Power Control: Reset':
            return True
        else:
            return False
    elif ipmi_type == "on":
        if msg == 'Chassis Power Control: Up/On':
            return True
        else:
            return False
    elif ipmi_type == "off":
        if msg == 'Chassis Power Control: Down/Off':
            return True
        else:
            return False
    elif ipmi_type == "status":
        return msg
    else:
        raise Exception("wrong type")


def write_to_file(content, file, clear=None):
    with open(file, "a") as f:
        if clear:
            f.truncate(0)
        f.write(content)


def sub_process(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, *args, **kwargs):
    subprocess.run(cmd, shell=shell, stdout=stdout, stderr=stderr,
                   )


def get_command_arg(*arguments):
    """
    获取命令行参数
    :param arguments: [{"name":"-tag","required":True},{"name":"--dog","required":False},{"name":"--cat"}]
    :return:Namespace(dog=None,cat=None,tag='dhyx-round-2')
    """
    parser = argparse.ArgumentParser()
    for arg in arguments:
        if "required" in arg:
            if arg["required"]:
                required = True
            else:
                required = False
        else:
            required = False
        parser.add_argument("{}".format(arg["name"]), required=required)
    return parser.parse_args()


def image_base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def judge_files_download_completely(scenario_image_path, image_num):
    n_time = time.time()
    file_length = None
    while True:
        try:
            file_length = len(os.listdir(scenario_image_path))
        except Exception:
            pass

        if file_length == image_num:
            size = os.path.getsize(scenario_image_path)
            time.sleep(5)
            size_next = os.path.getsize(scenario_image_path)
            if size == size_next:
                break
        if time.time() - n_time > 10 * 60:
            raise Exception("图片下载失败")
    return True


def get_frame_index(callback_msg, frame_rate=25):
    relative_time = float(get_item_by_key(callback_msg, "relative_time")[0:-1])
    frame_index_f, frame_index_i = math.modf(relative_time * frame_rate)
    if frame_index_f > 0.5:
        frame_index = int(math.ceil(relative_time * frame_rate))
    else:
        frame_index = str(int(frame_index_i))
    return frame_index


def download_image(image_host, file_name, image_path, image_num):
    cmd = f"sshpass -p Goodsense1 scp -r root@{image_host}:/root/videos/image/{file_name} {image_path}"
    os.popen(cmd)

    scenario_image_path = os.path.join(image_path, file_name)
    if judge_files_download_completely(scenario_image_path, image_num):
        image_names = os.listdir(scenario_image_path)
    else:
        raise Exception("图片未下载完成")
    return image_names


def download_algorithm_app_file(host, file_name, image_path, image_num):
    cmd = f"sshpass -p Goodsense scp -r root@{host}:/root/algorithm/{file_name} {image_path}"
    os.popen(cmd)

    scenario_image_path = os.path.join(image_path, file_name)
    if judge_files_download_completely(scenario_image_path, image_num):
        image_names = os.listdir(scenario_image_path)
    else:
        raise Exception("算法仓文件未下载完成")
    return image_names


def get_image_path_generator(path):
    img_formats = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.dng']
    p = Path(path)
    generator_images = p.rglob('*.*')
    return generator_images, img_formats


def aio_http_retry(*exceptions, retries=60, calm_down=60):
    """Decorate an async function to execute it a few times before giving up.
    Hopes that problem is resolved by another side shortly.

    Args:
        exceptions (Tuple[Exception]) : The exceptions expected during function execution
        retries (int): Number of retries of function execution.
        calm_down (int): Seconds to wait before retry.
    """

    def wrap(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            retries_count = 0

            while True:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except exceptions as err:
                    retries_count += 1
                    if retries_count >= retries:
                        return err

                    if calm_down:
                        await asyncio.sleep(calm_down)

        return inner

    return wrap


@aio_http_retry(aiohttp.ClientConnectionError, aiohttp.ClientResponseError, aiohttp.ClientPayloadError,
                aiohttp.InvalidURL, retries=60, calm_down=60)
async def asynchronous_get(session, url):
    async with session.get(url) as response:
        return await response.json()


@aio_http_retry(aiohttp.ClientConnectionError, aiohttp.ClientResponseError, aiohttp.ClientPayloadError,
                aiohttp.InvalidURL, retries=60, calm_down=60)
async def asynchronous_post(session, url, json_request_body=None):
    async with session.post(url, json=json_request_body) as response:
        return await response.json()
