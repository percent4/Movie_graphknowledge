# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-03-14 20:53
import os, re, json, traceback
from pprint import pprint

from triple_extract.triple_extractor import TripleExtract


text = "真人版的《花木兰》由新西兰导演妮基·卡罗执导，由刘亦菲、甄子丹、郑佩佩、巩俐、李连杰等加盟，几乎是全亚洲阵容。"
text = "公开资料显示，李强，男，汉族，出生于1971年12月，北京市人，北京市委党校在职研究生学历，教育学学士学位，1996年11月入党，1993年7月参加工作。"

triple_extract = TripleExtract(text)
print("原文： %s" % text)
entities = triple_extract.get_entity()
print("实体： ", end='')
pprint(entities)

spo_list = triple_extract.extractor()
print("三元组： ", end='')
pprint(spo_list)
