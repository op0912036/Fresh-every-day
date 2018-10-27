import pymysql

# 使用pymysql代替mysqldb
pymysql.install_as_MySQLdb()


'''
启动nginx
sudo /usr/local/nginx/sbin/nginx

启动redis
sudo redis-server /etc/redis/redis.conf

启动fastDFS
sudo /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf
sudo /usr/bin/fdfs_storaged /etc/fdfs/storage.conf
'''