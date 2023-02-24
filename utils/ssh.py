# -*- coding: utf-8 -*-
import paramiko
import asyncssh
import asyncio

__all__ = ['SSH', 'AsyncSSH', 'inquire_server_run_node_ip']


class SSH:
    def __init__(self, ip, user, password, port=22):
        self.ip = ip
        self.user = user
        self.password = password
        self.ssh = None
        self.stdin = None
        self.stderr = None
        self.stdout = None
        self.port = port
        self.conn()

    def conn(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.ip, username=self.user, password=self.password, timeout=1, port=self.port)
        except Exception as e:
            print(e)
            self.ssh = None

    def run(self, cmd):
        # print(cmd)
        if self.ssh:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=60 * 10)
            self.stdin = stdin
            self.stderr = stderr
            self.stdout = stdout
            return stdout
        else:
            return '%s@%s:%s ssh connect failed!' % (self.ip, self.user, self.password)

    def run_cmd(self, cmd):
        # 新增的run方法，返回值直接是列表，每行对应linux的输出；替代上面的run方法
        # print(cmd)
        if self.ssh:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=60 * 10)
            self.stdin = stdin
            self.stderr = stderr
            self.stdout = stdout
            return [elem[:-1] for elem in stdout.readlines()]
        else:
            return []

    def run_cmd_stderr(self, cmd):
        # 新增的run方法，返回值直接是列表，每行对应linux的输出返回stderr的输出
        if self.ssh:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=60 * 10)
            self.stdin = stdin
            self.stderr = stderr
            self.stdout = stdout
            return [elem[:-1] for elem in stderr.readlines()]
        else:
            return []

    def run_status(self, cmd, log=None):
        # 返回执行命令的状态
        if self.ssh:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=60 * 10)
            stderr_info = stderr.readlines()
            if stderr_info:
                log.info("run cmd=%s failed!! Error info was %s" % (cmd, stderr_info))
                return False
            return True
        else:
            log.info('%s@%s:%s ssh connect failed!' % (self.ip, self.user, self.password))
            return False

    def connect_withtrans(self):
        # 连接一个trans 通道， 用来上传和下载文件
        transport = paramiko.Transport(self.ip + ':' + str(22))
        transport.connect(username=self.user, password=self.password)
        self.__transport = transport

    def upload_file(self, local_path, remote_path):
        # 向远程服务器上传一个文件
        self.connect_withtrans()

        # sftp.chmod(target_path, 0o755)
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, remote_path, confirm=True)
        sftp.chmod(remote_path, 0o755)
        sftp.close()

    def download_file(self, remote_path, local_path):
        # 向远程服务器下载一个文件
        self.connect_withtrans()
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)
        sftp.close()

    def close(self):
        if self.ssh:
            self.ssh.close()


class AsyncSSH:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.ssh = None

    async def conn(self):
        self.ssh = await asyncssh.connect(self.ip, username=self.user, password=self.password, known_hosts=None)

    async def run_cmd(self, cmd, retry=30):
        try:
            if not self.ssh:
                await self.conn()
            result = await self.ssh.run(cmd, check=True)
            # print(cmd)
            return result.stdout.splitlines()
        except Exception as e:
            if retry == 0:
                raise e
            await asyncio.sleep(0.1)
            return await self.run_cmd(cmd, retry - 1)


def inquire_server_run_node_ip(host, key, user='root', password='V1p3r1@#$%'):
    """
    查询pod运行在哪个NODE节点上
    :param host: 测试机HOST
    :param user: 测试机用户名
    :param password: 测试机密码
    :param key: 查询pod的命令，如：查询egress，kubectl get pod -o wide | grep  egress
    :return: 实际运行在NODE节点的IP
    """
    hosts_list = []
    ssh = SSH(host.split(':')[0], user, password)
    ssh.conn()
    hostname = ssh.run_cmd(key + "| awk '{0}'".format('{print $7}'))
    if hostname == '':
        raise Exception("获取NODE_NAME失败，请检查查询命令是否正确")
    for i in hostname:
        hosts = ssh.run_cmd('kubectl describe nodes {0} | grep InternalIP'.format(i))[0]
        hosts_list.append(hosts.split(":")[-1].strip())
    node_ip = list(set(hosts_list))
    return node_ip
