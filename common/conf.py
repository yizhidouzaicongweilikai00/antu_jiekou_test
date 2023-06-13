from common.utils import Utils


class GlobalConf:
    env = Utils.get_env()
    domain = Utils.get_env_conf("domain")