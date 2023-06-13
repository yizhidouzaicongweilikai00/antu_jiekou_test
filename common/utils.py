import os
import configparser


class ConfigParse(configparser.RawConfigParser):
    '''
    框架中底层所使用的方法，业务一般不建议使用，解析器，用于解析config文件
    '''

    def __init__(self, defaults=None):
        configparser.RawConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class Utils(object):
    @staticmethod
    def get_conf(section, key):
        '''
        框架中底层所使用的方法，业务可以使用，用于读取指定conf文件下的key，使用方法：Utils().get_conf(section='boe', key='header')
        :param section: section区域
        :param key: key值
        :return:
        '''
        file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", f"conf.ini")
        config = ConfigParse()
        config.read(file)
        try:
            return config[section][key]
        except KeyError:
            raise KeyError(f"conf.ini, section:{section},key:{key} not found, please check!")

    @staticmethod
    def get_header_conf(section):
        '''
        框架中底层所使用的方法，业务可以使用，用于读取指定conf文件下的key，使用方法：Utils().get_header_conf(section='boe')
        :param section: section区域
        :return: dict
        '''
        file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", f"conf.ini")
        config = ConfigParse()
        config.read(file)
        return dict(config._sections)[section]

    @staticmethod
    def get_env():
        '''
        框架中底层所使用的方法，业务可以使用，用于获取当前的env环境，使用方法:Utils().get_env()
        :return:
        '''
        if os.getenv("env"):
            return os.getenv("env")
        else:
            return Utils.get_conf("common", "env")

    @staticmethod
    def get_env_conf(key):
        return Utils.get_conf(Utils.get_env(), key)

    @staticmethod
    def get_env_confs():
        return Utils.get_header_conf(Utils.get_env())

    @staticmethod
    def get_common_conf(key):
        return Utils.get_conf("common", key)

    @staticmethod
    def get_project_dir():
        return os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

    @staticmethod
    def get_component_profile_dir():
        return Utils.get_project_dir() + "/resources/profile/"

    @staticmethod
    def get_env_data_dir():
        return Utils.get_project_dir() + "/resources/data/" + Utils.get_env()
