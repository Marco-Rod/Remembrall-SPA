"""
Settings for the flask application object
"""

class BaseConfig(object):
    POSTGRES = {
        'user':'postgres',
        'pw': '',
        'db':'remembrall',
        'host': 'localhost',
        'port': '5432',
    }

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'i3c2xs%z4sk=9mts8)=8_u+=fng_d+gv7u$yp-zewz#kx#rn9f'
    