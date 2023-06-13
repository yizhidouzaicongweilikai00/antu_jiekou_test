import traceback
from functools import wraps
from common.logger import get_logger
from common.utils import Utils
from common.conf import GlobalConf
from common.bytecontext import *
from common.context_util import ContextUtil
import json


def assert_status_200(func):
    @wraps(func)
    def assert_200(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            assert result.status_code == 200, f"请求失败! 失败的resp为: {result.text}"
            return result
        except Exception as e:
            get_logger().error(
                f"httpclient.{func.__name__} 请求报错, 参数: {e.args}, 报错信息: {traceback.format_exc()}")
            raise e

    return assert_200


def log_func(func):
    '''
    装饰器，业务可以直接使用，主要是打印当前运行了什么方法
    :param func: 函数名称
    :return:
    '''

    @wraps(func)
    def log(*args, **kwargs):
        try:
            print("当前运行方法: ", func.__name__)
            return func(*args, **kwargs)
        except Exception as e:
            get_logger().error(f"{func.__name__} is error, logId: {e.args},  errMsg is: {traceback.format_exc()}")

    return log


def log_byterunner(func):
    @wraps(func)
    def log(*args, **kwargs):
        component = args[1].component
        get_logger().info(
            f"{component.type.name}开始执行, 方法={component.method}, 地址为={component.url}, 执行环境为={Utils.get_env()}, 请求参数为={component.byterequest.body}")
        result = func(*args, **kwargs)
        if Utils.get_common_conf("pretty_print").lower() == "true":
            result_print = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            result_print = result
        get_logger().info(f"{component.type.name}执行结束, logid={args[1].logid}, 返回结果={result_print}")
        return result

    return log


def component(profile_path=None):
    def _component(func):
        @wraps(func)
        def spec(*args, **kwargs):
            for arg in args:
                if isinstance(arg, ByteContext):
                    context = args[1]
                    context.component = ContextUtil.build_component(context, profile_path)
            return func(*args, **kwargs)

        return spec

    return _component
