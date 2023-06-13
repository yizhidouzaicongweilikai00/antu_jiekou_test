import jsonschema

from common.context_util import ContextUtil
from common.httpclient import VolcengineHttpClient
from common.bytecontext import *
from common.decorators import log_byterunner
import inspect

from common.logger import get_logger
from common.utils import Utils


class ByteRunner(object):
    _IAD_HTTP_CLIENT = VolcengineHttpClient()

    def execute(self, context: ByteContext, profile_path=None):
        '''
        :param context:测试上下文
        :param profile_path:组件定义文件路径
        :return:
        '''
        stack = inspect.stack()
        result_path = stack[2].function

        # 如果传了组件定义文件，则重新生成要执行的组件信息
        if profile_path:
            ContextUtil.build_component(context, profile_path)

        '''先清空上次的执行结果'''
        context.result = None
        context.logid = None

        component = context.component
        msg = f"{component.type.name}开始执行, 方法={component.method}, 地址={component.url}, 执行环境={Utils.get_env()}, 请求参数={component.byterequest}"
        get_logger().info(msg)

        context.result = self._IAD_HTTP_CLIENT.execute(context)

        dumps_indent = None
        if Utils.get_common_conf("pretty_print").lower() == "true":
            dumps_indent = 2
        result_print = json.dumps(context.result, indent=dumps_indent, ensure_ascii=False)
        msg = f"{component.type.name}执行结束, logid={context.logid}, 返回结果={result_print}"
        get_logger().info(msg)

        if (context.result.get("errNo") == 0) and (component.schema):
            jsonschema.validate(context.result, component.schema)

        context.component = None
        context.output[result_path] = context.result

        return context.result
