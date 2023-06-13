import urllib3
import requests
import json
from requests.adapters import HTTPAdapter
from common.bytecontext import ByteContext
from common.decorators import assert_status_200
from common.logger import get_logger
from common.conf import GlobalConf

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_LOGIN_COOKIES = {}
LOGGER = get_logger()


class VolcengineHttpClient(object):

    def __init__(self, timeout=5):
        """
        :param timeout: 每个请求的超时时间
        """
        s = requests.Session()
        #: 在session实例上挂载Adapter实例, 目的: 请求异常时,自动重试
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        #: 设置为False, 主要是HTTPS时会报错, 为了安全也可以设置为True
        s.verify = True
        #: 挂载到self上面
        self.s = s
        self.timeout = timeout

    def execute(self, context: ByteContext):

        login_identity = context.input.get("loginIdentity")
        '''全局登陆逻辑，只要传了loginIdentity都会先进行登陆操作'''
        login_info = _LOGIN_COOKIES.get(login_identity) if login_identity else None
        if login_identity and login_info is None:
            login_context = ByteContext(context.input.copy())
            _LOGIN_COOKIES[login_identity] = self.get_logined_cookie(login_context)

        component = context.component
        byterequest = component.byterequest
        '''只有传了账号才会需要添加登陆态信息'''
        if login_identity:
            byterequest.headers["x-csrf-token"] = _LOGIN_COOKIES[login_identity][0]
            byterequest.headers["cookie"] = _LOGIN_COOKIES[login_identity][1]

        response = None
        if component.method == "POST":
            response = self.post(url=component.url, json_data=byterequest.body, params=byterequest.query_params,
                                 headers=byterequest.headers)
        elif component.method == "GET":
            response = self.get(url=component.url, json_data=byterequest.body, params=byterequest.query_params,
                                headers=byterequest.headers)
        context.logid = response.headers.get("X-Tt-LogId", None)
        return json.loads(response.text)

    def get_logined_cookie(self, context: ByteContext):
        loginIdentity = context.input["loginIdentity"]
        LOGGER.info(f"--登陆逻辑处理--账号{loginIdentity}未登陆，开始进行登陆")

        json_data = {"Identity": loginIdentity}
        url = GlobalConf.domain + "/api/common/passport/getRandomSalt"
        response = self.post(url=url, json_data=json_data)
        result = json.loads(response.text)

        password = context.input["loginPassword"] + result["Result"]["Ticket"]
        json_data = {"Identity": loginIdentity, "DataRangersLogin": False, "Password": password}
        url = GlobalConf.domain + "/api/common/passport/login"
        response = self.post(url=url, json_data=json_data)
        result = json.loads(response.text)

        assert result["ResponseMetadata"].get(
            "Error") is None, f"--登陆逻辑处理--账号{loginIdentity}登陆失败，{result['ResponseMetadata']['Error']}"

        cookie = ""
        csrf_token = ""
        for name, value in response.cookies.items():
            cookie += "{0}={1};".format(name, value)
            if name == "csrfToken": csrf_token = value
        LOGGER.info(f"--登陆逻辑处理--账号{loginIdentity}登陆成功, cookie值:{cookie}")

        return csrf_token, cookie

    @assert_status_200
    def get(self, url=None, params=None, json_data=None, headers=None):
        return self.s.get(url=url, params=params, json=json_data, headers=headers, timeout=self.timeout)

    @assert_status_200
    def post(self, url=None, json_data=None, params=None, headers=None):
        return self.s.post(url=url, json=json_data, params=params, headers=headers, timeout=self.timeout)

    @assert_status_200
    def delete(self, url=None, params=None, json_data=None, headers=None):
        return self.s.delete(url=url, json=json_data, params=params, headers=headers, timeout=self.timeout)

    def __del__(self):
        if self.s:
            self.s.close()
