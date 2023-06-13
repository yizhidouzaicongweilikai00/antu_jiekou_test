import allure
import pytest
import jsonpath
from component.api.launch_task_api import LaunchTaskAPI
from common.context_util import ContextUtil
from common.bytecontext import *
from common.assert_util import AssertUtil


@allure.feature("投放管理-投放任务")
class TestLaunchTask(object):

    @allure.story("查询投放任务模板列表成功")
    @allure.description("查询场景包括：默认条件、单参数查询、多参数组合查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.Online
    @ContextUtil.parameters("/launch_manage/launch_task.json")
    def test_search_live_templates_success(self, context: ByteContext):
        with allure.step("请求接口"):
            LaunchTaskAPI().search_live_templates(context)
        with allure.step("校验返回码为成功"):
            AssertUtil.assert_success(context.result)
        with allure.step("校验查询返回结果与查询参数一致"):
            for field in context.input["checkFields"]:
                actual_fields = set(jsonpath.jsonpath(context.result, "$..{0}".format(field)))
                for actual_field in actual_fields:
                    assert actual_field in context.input[field], "返回数据与查询参数值不匹配"
