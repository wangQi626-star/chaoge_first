import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='lichao123')
cursor = conn.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS resume_generator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
conn.close()
print('数据库创建成功')
