import os
DEBUG=True
SECRET_KEY=os.urandom(24)
DIALECT='mysql'
DRIVER='mysqldb'
USERNAME='root'
PASSWORD='xxx'
HOST='193.112.41.211'
PORT='3306'
DATABASE='blog'

SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS=True


MAIL_SERVER='smtp.qq.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME='x'
MAIL_PASSWORD='x'
MAIL_DEFAULT_SENDER=('x','x')

DEBUG_TB_INTERCEPT_REDIRECTS=False

KKLOG_POST_PER_PAGE=20
WHOOSHEE_MIN_STRING_LEN=1
