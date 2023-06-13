import json_tools


class AssertUtil(object):

    @staticmethod
    def assert_success(result):
        assert result.get("errNo") == 0, "期望errNo等于0，实际为{0}".format(result.get("errNo"))

    @staticmethod
    def assert_len_not_zero(data, desc=""):
        '''
        断言数据长度的是否大于0，数据类型可为list、dict
        '''
        assert len(data) > 0, f"期望{desc}数据长度大于0，实际为0"

    @staticmethod
    def assert_json(actual, expected):
        diff_result = json_tools.diff(actual, expected)
        adds = []
        replaces = []
        for diff_info in diff_result:
            if diff_info.get("add"):
                adds.append(diff_info.get("add"))
            if diff_info.get("replace"):
                replaces.append(
                    f"字段{diff_info.get('replace')}不匹配，期望={diff_info.get('value')}, 实际={diff_info.get('prev')}")
        is_success = (len(adds) == 0) and (len(replaces) == 0)
        error_info = ""
        if adds:
            error_info += f"缺少字段:{adds}\n"
        for replace in replaces:
            error_info += replace + "\n"
        assert is_success is True, error_info