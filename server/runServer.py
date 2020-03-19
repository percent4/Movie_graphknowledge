# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-03-18 14:09
import json
import traceback
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import datetime
import pymysql
import logging.config

from triple_extract.triple_extractor import TripleExtract

# 定义端口为9009
define("port", default=6007, help="run on the given port", type=int)

# 日志控制

CONF_LOG = "../conf/logging.conf"
logging.config.fileConfig(CONF_LOG)
logger = logging.getLogger()



# Handler
class QueryHandler(tornado.web.RequestHandler):

    # get函数
    def get(self):
        self.render('index.html')


# 预测页面
class ExtractHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):

        try:
            document = self.get_argument("event").replace(' ', '')
            logger.info("原文：%s" % document)
            triple_extract = TripleExtract(document)
            spo_list = triple_extract.extractor()


            self.render('extract.html',
                        sent=document,
                        spos='\r\n'.join(['#'.join(_) for _ in spo_list])
                        )

        except Exception:
            logger.error(traceback.format_exc())

    def post(self):

        try:
            # 获取前端参数
            document = self.get_argument("event").replace(' ', '')
            spo = self.get_argument("spo")
            is_mysql = self.get_argument("is_mysql")

            print(spo)
            print(is_mysql)
            logger.info("抽取三元组信息： \n%s" % json.dumps(spo.split("\r\n"), ensure_ascii=False, indent=2))
            logger.info("是否导入数据库： %s" % is_mysql)

            # 将数据导入至数据库
            if is_mysql == "1":
                # 读取三元组信息
                subjects = []
                predicates = []
                objects = []

                for item in spo.split("\r\n"):
                    subj, pred, obj = item.split("#")
                    if subj and pred and obj:
                        subjects.append(subj)
                        predicates.append(pred)
                        objects.append(obj)

                # 创建数据库记录
                records = []
                if subjects and predicates and objects:
                    for subj, pred, obj in zip(subjects, predicates, objects):
                        records.append([datetime.datetime.now(), subj, pred, obj, document])



                # 打开数据库连接
                db = pymysql.connect("localhost", "root", "", "movie_graph")

                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = db.cursor()

                # 使用executemany插入

                sql = """INSERT INTO movies
                          (create_time, subject, predicate, object, document)
                         VALUES
                         (%s,%s,%s,%s,%s)
                      """

                try:
                    cursor.executemany(sql, records)
                    db.commit()  # 有数据插入或删除时需用commit()
                except:
                    db.rollback()

                self.write("<script>alert('成功导入%d条记录至MySQL数据库。')</script>" % len(records))
                logger.info("成功导入%d条记录至MySQL数据库。" % len(records))

        except Exception:

            self.write("<script>alert('导入失败，请前往日志查看。')</script>")
            logger.error(traceback.format_exc())

        finally:

            self.render('index.html')


# 主函数
def main():
    # 开启tornado服务
    tornado.options.parse_command_line()
    # 定义app
    app = tornado.web.Application(
            handlers=[(r'/index', QueryHandler),
                      (r'/extract', ExtractHandler)
                      ], #网页路径控制
            template_path=os.path.join(os.path.dirname(__file__), "templates")  # 模板路径
          )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


main()