import pytest
from interface.business import task_management
from utils.query import query_payload, query_device_id, query_task_id


class Test_cam_task:

    def setup_class(self):
        self.device_id = query_device_id('CAM')
        self.incidentTypes = "INCIDENT_CROWD"
        self.request_body_cam_task_create = query_payload('add_cam_task')
        self.request_body_query_cam_alert = query_payload('query_cam_alert')
        self.request_body_cam_search_center = query_payload('cam_search_center')

    def teardown(self):
        """
        清理自动化测试环境
        :return:
        """
        pass

    @pytest.mark.skipif(condition=0 > 1, reason="跳过该函数")
    def test_create_cam_task(self):
        request_body = self.request_body_cam_task_create
        request_body["deviceTaskConfigs"][0]["deviceId"] = query_device_id("CAM")
        resp, url = task_management.TaskManagement().add_face_attr_task(**request_body)
        assert resp["content"][
                   "message"] == "success", f"create cam_task failed,request body is :{request_body},\nreason:{resp['content']['message']}"

    # @pytest.mark.skipif(condition=2 > 1, reason="跳过该函数")
    def test_cam_task_alert(self):
        request_body = self.request_body_query_cam_alert
        request_body["deviceIds"][0] = self.device_id
        resp, url = task_management.TaskManagement().query_alert(**request_body)
        assert resp["content"]["data"][
                   "total"] > 0, f"cam_task query no alert,request body is :{request_body},\nreason:{resp['data']['message']}"

    # @pytest.mark.skip()
    def test_cam_task_search_center(self):
        request_body = self.request_body_cam_search_center
        request_body["deviceIdList"][0] = self.device_id
        resp, url = task_management.TaskManagement().query_search_center(**request_body)
        assert resp["content"]["data"]["searchList"][0][
                   "total"] > 0, f"cam_task query no data,request body is :{request_body},\nreason:{resp['data']['message']}"

    # @pytest.mark.skip()
    def test_cam_task_delete(self):
        task_id = query_task_id(self.device_id)
        resp, url = task_management.TaskManagement().delete_task(task_id)
        assert resp["content"]["message"] == "success", f"delete cam_task failed,\nreason:{resp['content']['message']}"
