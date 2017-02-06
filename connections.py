import MySQLdb
import os


def on_appengine():
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine')


def connection():
    # db_ip = "173.194.238.206"
    db_user = os.getenv('CLOUD_SQL_USER')
    db_pass = os.getenv('CLOUD_SQL_PASS')

    if on_appengine():
        instance_id = "user-login-1234:user-login"  # os.getenv('CLOUD_SQL_INSTANCE_ID')
        sock = "/cloudsql/{}".format(instance_id)
        conn = MySQLdb.connect(unix_socket="/cloudsql/" + instance_id, db="users",
                               user="root", passwd=db_pass)
    else:
        '''
        db_ip = "173.194.238.206"
        conn = MySQLdb.connect(host=db_ip, db="users",
                               user=db_user, passwd=db_pass)
        '''

        '''
        conn = MySQLdb.connect(host="173.194.238.206",
                               user="suraj",
                               passwd="surajkamble",
                               db="users")
        '''
        db_ip = os.getenv('CLOUD_SQL_IP')
        conn = MySQLdb.connect(host=db_ip, db="users",
                               user=db_user, passwd=db_pass)

    c = conn.cursor()

    return c, conn