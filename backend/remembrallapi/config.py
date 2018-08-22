"""
Settings for the flask application object
"""


class BaseConfig(object):

    POSTGRES_URL = 'mydb-instance.cqak9rvjxgdz.us-east-2.rds.amazonaws.com:5432'
    POSTGRES_USER = 'marco'
    POSTGRES_PW = 'marcorodriguez'
    POSTGRES_DB = 'remembrall'
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "i3c2xs%z4sk=9mts8)=8_u+=fng_d+gv7u$yp-zewz#kx#rn9f"
