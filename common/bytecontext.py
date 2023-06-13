from enum import Enum
import json

import jsonpath


class ByteComponent(object):

    def __init__(self, type=None, url=None, method=None, byterequest=None, schema=None):
        if type is None:
            type = RequestType.HTTP
        self.type = type
        self.url = url
        self.method = method
        self.byterequest = byterequest
        self.schema = schema

    @staticmethod
    def dict2component(dict):
        dict_request = dict['request']
        byterequest = ByteRequest(dict_request.get("bodyType"), dict_request.get('headers'),
                                  dict_request.get('queryParams'), dict_request.get('body'))
        schema = dict.get("schema")
        return ByteComponent(RequestType.get(dict["type"]), dict['url'], dict['method'], byterequest, schema)


class RequestType(Enum):
    HTTP = "HTTP"
    RPC = "RPC"

    @staticmethod
    def get(value):
        value = value.upper()
        return RequestType(value) if value in RequestType.__members__.keys() else None


class ByteRequest(object):

    def __init__(self, body_type, headers, query_params, body):
        self.body_type = body_type
        self.headers = headers
        self.query_params = query_params
        self.body = body

    def __str__(self):
        return str({**self.query_params, **self.body})


class ByteContext(object):
    TEST_DATA_DECS_KEY = "__testDataDesc"

    def __init__(self, data=None):
        if data is None:
            data = {}
        # 输入数据，包括入参、期望校验值等测试场景需要用到的参数
        self.input = data
        # 输出数据，用于存在接口返回值、特殊字段提取等
        # 每次接口调用会自动存放返回数据，key为组件函数名
        self.output = {}
        # 最近一次组件调用返回的logid
        self.logid = None
        # 最近一次组件调用的返回数据
        self.result = None
        # 即将要调用执行的组件信息
        self.component = None

    def get_input(self, key):
        return self.input.get(key)

    def add_input(self, key, value):
        self.input.update({key: value})

    def get_output(self, key):
        return self.output.get(key)

    def get_result(self, path, return_list=False):
        '''
        :param path: jsonpath路径
        :param return_list: 默认返回单个值，如果预期查找的数据是个列表，请传True
        :return:
        '''
        value = jsonpath.jsonpath(self.result, path)
        if not value:
            raise Exception("无法找到对应的字段值，请确认json路径是否正确")
        return (value if return_list else value[0])

    def __str__(self):
        return json.dumps(self.input, ensure_ascii=False)
