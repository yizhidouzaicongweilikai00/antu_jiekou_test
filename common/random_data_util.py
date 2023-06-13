import random
import string

from common.date_util import DateUtil


class RandomDataUtil(object):
    '''
    用于生成随机参数的函数，可在data文件直接使用
    '''

    @staticmethod
    def random_string(len):
        return ''.join(random.sample(string.ascii_letters + string.digits, len))

    @staticmethod
    def get_now_second_string():
        return DateUtil.get_now_string()
