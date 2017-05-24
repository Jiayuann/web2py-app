
if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)


db=DAL("sqlite://storage.sqlite")

auth=Auth(db)
auth.define_tables(username=True)

db.define_table(
    'forsale',
    Field('user_name',db.auth_user,default=auth.user_id),
    Field('seller_name'),
    Field('email'),
    Field('phone_number'),
    Field('date_posted','date'),
    Field('price','double'),
    Field('title',unique=True),
    Field('description','text'),
    Field('image','upload'),
    Field('category'),

    Field('is_available','boolean',default=False),
    ###defines a format string for the table.It determines how a record should be represented as a string
    format='%(title)s'
)

db.forsale.email.requires=IS_EMAIL()
db.forsale.phone_number.requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$',error_message='Example: (831)3461111')
db.forsale.title.requires=IS_NOT_IN_DB(db,db.forsale.title)
db.forsale.category.requires=IS_IN_SET(["Car","Bike","Book","Music","Outdoors","Household","Misc"],zero=T('choose one'))
db.forsale.price.requires=IS_FLOAT_IN_RANGE(0,100000.0,error_message='The price should be in the range 0..1000000')


auth=Auth(db)
auth.define_tables(username=True)
