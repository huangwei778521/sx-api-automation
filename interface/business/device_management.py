from config.host_info import host_info_url, host_info_header
from config.business.url import business_path
from utils.request import Request


class DeviceManagement:
    def __init__(self):
        self.url = host_info_url
        self.header = host_info_header
        self.path = business_path.get('DeviceManagement')

    def add_device_group(self, **request_body):
        """
        :param request_body:
        :return:
        """
        url = self.url + self.path.get("device_group_add")
        resp = Request(method="POST", url=url, headers=self.header,
                       json_data=request_body).request()
        return resp, url

    def device_add(self, **request_body):
        """
        :param request_body:
        :return:
        """
        url = self.url + self.path.get("device_add")
        resp = Request(method="POST", url=url, headers=self.header,
                       json_data=request_body).request()
        return resp, url
