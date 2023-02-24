from config.host_info import host_info_url, host_info_header
from config.business.url import business_path
from utils.request import Request


class TaskManagement:
    def __init__(self):
        self.url = host_info_url
        self.header = host_info_header
        self.path = business_path.get('TaskManagement')

    def add_face_attr_task(self, **request_body):
        """
        添加人脸属性任务
        :param request_body:
        :return:
        """
        url = self.url + self.path.get("face_attribute_add")
        resp = Request(method="POST", url=url, headers=self.header,
                       json_data=request_body).request()
        return resp, url

    def add_crowd_cam_task(self,**request_body):
        url = self.url + self.path.get("crowd_cam_add")
        resp = Request(method="POST", url=url, headers=self.header,
                       json_data=request_body).request()
        return resp, url

    def delete_task(self,task_id):
        url = self.url + self.path.get("task_delete").format(task_id)
        resp = Request(method="DELETE", url=url, headers=self.header,
                       ).request()
        return resp, url

    def query_alert(self,**request_body):
        url = self.url + self.path.get("query_alert")
        resp = Request(method="POST", url=url, headers=self.header,
                       json_data=request_body).request()
        return resp, url

    def query_search_center(self,**request_body):
        url = self.url + self.path.get("query_search_center")
        resp = Request(method="POST", url=url, headers=self.header,
                       json_data=request_body).request()
        return resp, url

    def query_attr_result(self,**request_body):
        url = self.url + self.path.get("face_attribute_query")
        resp = Request(method="POST", url=url, headers=self.header,
                       json_data=request_body).request()
        return resp, url
