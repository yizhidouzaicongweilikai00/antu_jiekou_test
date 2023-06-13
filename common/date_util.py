import time
import datetime


class DateUtil(object):
    SECOND_FORMAT = "%Y%m%d%H%M%S"

    @staticmethod
    def get_now_string(format=SECOND_FORMAT):
        return time.strftime(format, time.localtime())

    @staticmethod
    def get_today_timestamp() -> (int, int):
        '''
        框架中底层所使用的方法，业务可以使用，获取今日0点和今日24点的时间戳
        :return:
        '''
        begin_time = datetime.date.today()
        end_time = begin_time + datetime.timedelta(days=1)
        begin_time_stamp = int(time.mktime(time.strptime(str(begin_time), '%Y-%m-%d')))
        end_time_stamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d'))) - 1
        return begin_time_stamp, end_time_stamp

    @staticmethod
    def get_theweek_timestamp() -> (int, int):
        '''
        框架中底层所使用的方法，业务可以使用，获取本周周始0点和周末24点的时间戳
        :return:
        '''
        today = datetime.date.today()
        week = today.weekday()
        begin_time = today - datetime.timedelta(days=week)
        begin_time_stamp = int(time.mktime(time.strptime(str(begin_time), '%Y-%m-%d')))
        end_time = begin_time + datetime.timedelta(days=5)
        end_time_stamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d'))) - 1
        return begin_time_stamp, end_time_stamp

    @staticmethod
    def get_themonth_timestamp() -> (int, int):
        '''
        框架中底层所使用的方法，业务可以使用，获取本月月始0点和月末24点的时间戳
        :return:
        '''
        today = datetime.date.today()
        days = today.day - 1
        begin_time = today - datetime.timedelta(days=days)
        begin_time_stamp = int(time.mktime(time.strptime(str(begin_time), '%Y-%m-%d')))
        end_time = today + datetime.timedelta(days=1)
        end_time_stamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d'))) - 1
        return begin_time_stamp, end_time_stamp

    @staticmethod
    def get_now_timestamp() -> int:
        '''
        框架中底层所使用的方法，业务可以使用，获取当前时间点的时间戳
        :return:
        '''
        millis = int(round(time.time()) * 1000)
        return millis
