# -*- coding: utf-8 -*-
from commands import getstatusoutput
import datetime
import argparse
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf8')
sql_user = 'standard'  # 连接数据库用户
sql_passwd = "@fshJo2QFT^mCJ(*')"  # 连接数据库密码
now_time = datetime.datetime.now()
back_sql_name = "backup_" + now_time.strftime("%Y-%m-%d") + ".sql"  # 备份的文件名格式
log_name = "sql_back.log"  # 这里是日志文件名字格式
back_path = '/macrosan_backup/mysql_backup/'  # 备份文件存储位置
log_path = "{}{}".format(back_path, log_name)  # 日志文件存储位置
rm_time = '90'  # 自动删除备份文件


def arguments():
    '''
    这里是参数
    :return: 返回一个你调用脚本的时候传入的参数
    '''
    par = argparse.ArgumentParser(description="这个是数据库备份脚本")
    par.add_argument("--backup-all", "-b", action="store_true", help="数据库全备")
    par.add_argument("--restore", "-r", help="数据库还原")
    args = par.parse_args()
    return args


def log():
    '''
    这里是日志
    :return: 返回一个日志器对象
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("{}".format(log_path), encoding='utf-8')
    formatter = logging.Formatter(fmt="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def back():
    '''
    备份
    '''
    ret, tex = getstatusoutput(
        "mysqldump --single-transaction -u{} -p'{}' -h127.0.0.1 -P11306 --all-databases > {}{}".format(
            sql_user, sql_passwd, back_path,
            back_sql_name))
    if ret:
        logger.error(tex)
    else:
        logger.info("数据库备份成功")


def restore(res):
    '''
    还原
    :param res:传入还原所需的sql文件路径
    :return:
    '''
    ret, tex = getstatusoutput(
        "mysql -u{} -p'{}' -h127.0.0.1 -P11306 -e \"source {}\"".format(sql_user, sql_passwd, res))
    if ret:
        logger.error(tex)
    else:
        logger.info("数据库还原成功")


if __name__ == '__main__':
    arg = arguments()
    logger = log()
    getstatusoutput("rm -rf `find {} -name backup* +{}`".format(back_path, rm_time))
    if arg.backup_all:
        back()
    elif arg.restore:
        restore(arg.restore)
    else:
        print("你没有输入参数，加-h可以查看详细参数")
        
