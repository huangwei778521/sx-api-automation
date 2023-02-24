import pytest
from pytest_assume.plugin import assume
from interface.business import device_management
from config.server_info import server_info,file_path
from utils.query import read_config,query_payload


class Test_init_devices:

    def setup(self):
        self.device_names = read_config(file_path)
        self.host_info = server_info.get('host_info_26')
        self.request_body_add_group = query_payload('add_group')
        self.request_body_add_device = query_payload('add_device')

    @pytest.mark.run(order=1)
    @pytest.mark.skipif(condition=2 > 1, reason="跳过该函数")
    def test_add_device_group(self, root_group_id):
        request_body = self.request_body_add_group
        request_body["parentId"] = root_group_id
        resp, url = device_management.DeviceManagement().add_device_group(**request_body)
        assert (resp['content'][
                    'message'] == 'success',
                f"add device group failed,request body is :{request_body},reason:{resp['content']['message']}")

    @pytest.mark.run(order=2)
    @pytest.mark.skipif(condition=2 > 1, reason="跳过该函数")
    def test_add_devices(self, group_id):
        request_body = self.request_body_add_device
        for device in self.device_names:
            request_body["deviceName"] = device
            request_body["groupId"] = group_id
            request_body["rtspConfig"][
                "rtspAddress"] = f"rtsp://root:Goodsense@2021@{self.host_info['host']}:554/{device}"
            resp, url = device_management.DeviceManagement().device_add(**request_body)
            assume(resp['content'][
                       'message'] == 'success',
                   f"add devices failed,request body is:{request_body},reason:{resp['content']['message']}")


