import pymysql
pymysql.version_info = (1, 3, 13, "final", 0) # Django 识别版本号，所以将pymysql的版本号设置高一些
pymysql.install_as_MySQLdb() # 将pymysql作为mysqldb使用
