# Resource: https://www.attilatoth.dev/posts/flask-sqlalchemy-multiple-dbs/

#from getpass import getuser

#-------------VARIABLES---------------
Testing = False
#-------------------------------------


#------------CONSTANTS----------------
EMAIL_RECEIVER = ''
ETHERSCAN_API_KEY = ''
BLOCKNATIVE_API_KEY = ''
EMAIL_SENDER = 'eljacobsen12@gmail.com'
EMAIL_API_KEY = ''


#------------DATABASE SETUP------------
# Production Database.
class DbConfigProd(object):
    username = '' #getuser()
    password = ''
    hostname = f"{username}.mysql.pythonanywhere-services.com"
    databasename = f"{username}$rarity_distributions"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{username}:{password}@{hostname}/{databasename}"
    )
    SQLALCHEMY_BINDS = {
        'jobs': f"mysql://{username}:{password}@{hostname}/jobs",
        'collections': f"mysql://{username}:{password}@{hostname}/collections"
    }
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 299}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Development Database.
class DbConfigTest(object):
    username = '' #getuser()
    password = ''
    hostname = f"{username}.mysql.pythonanywhere-services.com"
    databasename = f"{username}$rarity_distributions_dev"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{username}:{password}@{hostname}/{databasename}"
    )
    SQLALCHEMY_BINDS = {
        'jobs': f"mysql://{username}:{password}@{hostname}/jobs",
        'collections': f"mysql://{username}:{password}@{hostname}/collections"
    }
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 299}
    SQLALCHEMY_TRACK_MODIFICATIONS = False