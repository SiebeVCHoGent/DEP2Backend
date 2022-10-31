from dotenv import dotenv_values
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

env = dict(dotenv_values())


class Config:
    def __init__(self):
        self.VERSION = Config.set_env_var("VERSION", "Not Specified")
        self.JWT_TOKEN = Config.set_env_var("JWT_TOKEN", "test_token")
        # Config Database
        self.DB_TYPE = Config.set_env_var("DB_TYPE", "postgresql")
        self.DB_USER = Config.set_env_var("DB_USER", "postgres")
        self.DB_PASSWORD = Config.set_env_var("DB_PASSWORD", "root")
        self.DB_HOST = Config.set_env_var("DB_HOST", "localhost")
        self.DB_NAME = Config.set_env_var("DB_NAME", "dataengineering")

    @staticmethod
    def set_env_var(env_name, default_value=None):
        env_value = env.get(env_name)
        if env_value is None and default_value is None:
            raise Exception(f"Environment variable {env_name} is not set")
        if env_value is None:
            return default_value
        return env_value


class DBConfig():
    def __init__(self, set):
        base = declarative_base()
        engine = create_engine(f'{set.DB_TYPE}://{set.DB_USER}:{set.DB_PASSWORD}@{set.DB_HOST}/{set.DB_NAME}')
        engine.connect()
        metadata = MetaData(engine)
        base.metadata.reflect(engine)

        class Kmo(base):
            __table__ = base.metadata.tables['kmo']
        self.Kmo = Kmo

        class Gemeente(base):
            __table__ = base.metadata.tables['gemeente']
        self.Gemeente = Gemeente

        class Sector(base):
            __table__ = base.metadata.tables['sector']
        self.Sector = Sector

        class Hoofdsector(base):
            __table__ = base.metadata.tables['hoofdsector']
        self.Hoofdsector = Hoofdsector

        class Verslag(base):
            __table__ = base.metadata.tables['verslag']
        self.Verslag = Verslag

        class Website(base):
            __table__ = base.metadata.tables['website']
        self.Website = Website

        class Jaarverslag(base):
            __table__ = base.metadata.tables['jaarverslag']
        self.Jaarverslag = Jaarverslag

        class User(base):
            __table__ = base.metadata.tables['user']
        self.User = User

        class Searchterm(base):
            __table__ = base.metadata.tables['searchterm']
        self.Searchterm = Searchterm

        Session = sessionmaker(bind=engine)
        self.session = Session()


settings = Config()
db = DBConfig(settings)
