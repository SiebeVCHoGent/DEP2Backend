from dotenv import dotenv_values
from sqlalchemy import create_engine, MetaData, Table
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
        self.DB_PORT = Config.set_env_var("DB_PORT", "5432")

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
        engine = create_engine(f'{set.DB_TYPE}://{set.DB_USER}:{set.DB_PASSWORD}@{set.DB_HOST}:{set.DB_PORT}/{set.DB_NAME}')
        engine.connect()
        metadata = MetaData(engine)
        base.metadata.reflect(engine)

        metadata2 = MetaData()


        class Kmo(base):
            __table__ = base.metadata.tables['kmo']
        self.Kmo = Kmo
        self.Kmo2 = Table('kmo', metadata2, autoload=True, autoload_with=engine)

        class Gemeente(base):
            __table__ = base.metadata.tables['gemeente']
        self.Gemeente = Gemeente
        self.Gemeente2 = Table('gemeente', metadata2, autoload=True, autoload_with=engine)

        class Sector(base):
            __table__ = base.metadata.tables['sector']
        self.Sector = Sector
        self.Sector2 = Table('sector', metadata2, autoload=True, autoload_with=engine)

        class Verslag(base):
            __table__ = base.metadata.tables['verslag']
        self.Verslag = Verslag
        self.Verslag2 = Table('verslag', metadata2, autoload=True, autoload_with=engine)

        class Website(base):
            __table__ = base.metadata.tables['website']
        self.Website = Website
        self.Website2 = Table('website', metadata2, autoload=True, autoload_with=engine)

        class Jaarverslag(base):
            __table__ = base.metadata.tables['jaarverslag']
        self.Jaarverslag = Jaarverslag
        self.Jaarverslag2 = Table('jaarverslag', metadata2, autoload=True, autoload_with=engine)

        class User(base):
            __table__ = base.metadata.tables['user']
        self.User = User
        self.User2 = Table('user', metadata2, autoload=True, autoload_with=engine)

        class Searchterm(base):
            __table__ = base.metadata.tables['searchterm']
        self.Searchterm = Searchterm
        self.Searchterm2 = Table('searchterm', metadata2, autoload=True, autoload_with=engine)

        class Score(base):
            __table__ = base.metadata.tables['zoektermscores']
        self.Score = Score
        self.Score2 = Table('zoektermscores', metadata2, autoload=True, autoload_with=engine)

        class Woord(base):
            __table__ = base.metadata.tables['woord']
        self.Woord = Woord
        self.Woord2 = Table('woord', metadata2, autoload=True, autoload_with=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()


settings = Config()
db = DBConfig(settings)
