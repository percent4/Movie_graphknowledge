### 影视类知识图谱构建

1. 安装requirements.txt中的模块；
2. 开启本地MySQL数据库，movie_graph数据库，表名为movies，表结构如下：

+-------------+----------+------+-----+---------+----------------+\
| Field       | Type     | Null | Key | Default | Extra          |\
+-------------+----------+------+-----+---------+----------------+\
| id          | int(11)  | NO   | PRI | NULL    | auto_increment |\
| create_time | datetime | YES  |     | NULL    |                |\
| subject     | text     | YES  |     | NULL    |                |\
| predicate   | text     | YES  |     | NULL    |                |\
| object      | text     | YES  |     | NULL    |                |\
| document    | text     | YES  |     | NULL    |                |\
+-------------+----------+------+-----+---------+----------------+

示例数据如下：

![](https://github.com/percent4/Movie_graphknowledge/blob/master/movie_db.png)

3. 启动"server/runServer.py"，在网页中输入"http://localhost:6007/index" .

