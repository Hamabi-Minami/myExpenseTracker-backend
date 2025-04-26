
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_name: str = 'My Blog'
    debug: bool = True
    db_url: str = 'mysql+pymysql://root:123456@localhost:32768/MA'
    secret_key: str = 'whl'
    algorithm:str = 'HS256'
    access_token_expire_minutes: int = 60 * 24 * 7 # expired in a week

    class Config:
        env_file = '.env'

settings = Settings()
