import base64

from utils.ssh import SSH
# from config.server_info import server_info

class K8sCluster:

    def get_host_user_password(self, server_info):
        """
        获取环境所有的服务用户名、密码
        :param server_info: 测试机主机信息
        :return: 以字典形式返回所有服务的用户名密码
        """
        host = server_info.get("host")
        user = server_info.get("user")
        password = server_info.get("password")

        ssh = SSH(host, user, password)
        ssh.conn()
        get_info_key = "kubectl get secret password-secrets -o yaml | sed -n '3,$p'"
        info_dir = {}
        infos = ssh.run_cmd(get_info_key)
        services = ["cassandra_admin_username", "cassandra_admin_password", "console_admin_username",
                    "console_admin_password", "gateway_admin_username", "gateway_admin_password",
                    "grafana_admin_username", "grafana_admin_password", "minio_admin_access_key",
                    "minio_admin_secret_key", "mysql_admin_username", "mysql_admin_password",
                    "mysql_batch_manager_username", "mysql_batch_manager_password", "mysql_camera_manager_username",
                    "mysql_camera_manager_password", "mysql_console_username", "mysql_console_password",
                    "mysql_gateway_username", "mysql_gateway_password", "mysql_storage_manager_username",
                    "mysql_storage_manager_password", "kafka_admin_password", "kafka_admin_username",
                    "mysql_root_username", "mysql_root_password"]

        for info in infos:
            if "kind" in info:
                break
            value = base64.b64decode(info.split(":")[-1].replace(" ", "")).decode("utf-8")
            key = info.split(":")[0].replace(" ", "")
            if key in services:
                info_dir[key] = value
        ssh.close()
        return info_dir


if __name__ == '__main__':
    server_info = {
            "host": "10.8.10.8",
            "user": "root",
            "password": "Goodsense@2021",
            "ipmi": "10.8.10.8"
        }
    Mytest = K8sCluster()
    info = Mytest.get_host_user_password(server_info)
    print(info)