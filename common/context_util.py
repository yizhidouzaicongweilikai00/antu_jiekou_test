from common.conf import GlobalConf
from common.utils import Utils
from common.bytecontext import *
import json
import pytest
import re

'''数据文件中引用的函数这里import，不可删除'''
from common.random_data_util import RandomDataUtil


class ContextUtil(object):
    _PATTERN = re.compile(r"\$FUNC\{[^\$\{\}]+\}")

    @staticmethod
    def process_function_expression(input_datas):
        if isinstance(input_datas, list):
            for i in input_datas:
                ContextUtil.process_function_expression(i)
        elif isinstance(input_datas, dict):
            for k in list(input_datas.keys()):
                if isinstance(input_datas[k], str) and "$FUNC{" in input_datas[k]:
                    for item in list(ContextUtil._PATTERN.findall(input_datas[k])):
                        value = eval(item[6:-1])
                        if input_datas[k] == item:
                            input_datas[k] = value
                        else:
                            input_datas[k] = input_datas[k].replace(item, str(value), 1)
                else:
                    ContextUtil.process_function_expression(input_datas[k])

    @staticmethod
    def preprocess_input(input_datas: list):
        # 替换测试数据中的函数表达式
        ContextUtil.process_function_expression(input_datas)
        # 添加全局数据
        '''添加配置，case层若已有则不覆盖'''

        global_confs = Utils.get_env_confs()
        for input_data in input_datas:
            for key in global_confs.keys():
                if input_data.get(key) is None:
                    input_data[key] = global_confs[key]

    @staticmethod
    def update_component_data(data, update):
        if not isinstance(data, dict):
            return
        for k in list(data.keys()):
            if isinstance(data[k], str) and data[k].startswith("${"):
                if update.get(data[k]) is not None:
                    data[k] = update.get(data[k])
                else:
                    del data[k]
            else:
                if isinstance(data[k], dict):
                    ContextUtil.update_component_data(data[k], update)
                if isinstance(data[k], list):
                    for i in data[k]:
                        ContextUtil.update_component_data(i, update)

    @staticmethod
    def parameters(data_path=None, key=None):
        if data_path:
            file_path = Utils.get_env_data_dir() + data_path
            with open(file_path, 'r') as f:
                dict = json.load(f)
            data = dict if key is None else dict[key]
            input_datas = data if isinstance(data, list) else [data]
        else:
            input_datas = [{}]
        ContextUtil.preprocess_input(input_datas)
        params = map(lambda x: pytest.param(ByteContext(x), id=x.get(ByteContext.TEST_DATA_DECS_KEY)), input_datas)
        return pytest.mark.parametrize("context", params)

    @staticmethod
    def build_component(context: ByteContext, profile_path):
        real_path = Utils.get_component_profile_dir() + profile_path
        with open(real_path, 'r') as f:
            dict = json.load(f)
            component = ByteComponent.dict2component(dict)
        component.url = GlobalConf.domain + component.url

        update = {}
        if context.input:
            update = {}
            for k in context.input.keys():
                k_new = "${" + k + "}"
                update.setdefault(k_new, context.input[k])
        ContextUtil.update_component_data(component.byterequest.body, update)
        ContextUtil.update_component_data(component.byterequest.query_params, update)
        context.component = component
        return component
