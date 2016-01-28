from configparser import SafeConfigParser
import os

config = SafeConfigParser()
config.read(os.path.join(os.path.dirname(__file__), os.pardir, 'alembic.ini'))
