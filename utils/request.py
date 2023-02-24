import json
import requests
from retry import retry


class Request:
    def __init__(self, url, method, headers=None, params=None, data=None, json_data=None, verify=None, files=None,
                 **kwargs):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.json_data = json_data
        self.files = files
        self.verify = verify
        self.kwargs = kwargs
        self.resp = None

    @retry(tries=10, delay=1)
    def request(self):
        self.resp = requests.request(method=self.method, url=self.url, headers=self.headers, params=self.params,
                                     data=self.data, json=self.json_data, verify=self.verify, files=self.files)
        if self.resp.status_code != 200:
            raise Exception(
                f"接口调用报错,url:{self.url},data:{self.data},params:{self.params},json_data:{self.json_data},resp:{self.resp}")
        self.resp = self.parse_resp()
        return self.resp

    def parse_resp(self):
        try:
            content = json.loads(self.resp.text)
        except Exception as e:
            content = self.resp.text

        resp = {
            "status_code": self.resp.status_code,
            "content": content,
            "headers": self.resp.headers,
            "reason": self.resp.reason
        }
        return resp
