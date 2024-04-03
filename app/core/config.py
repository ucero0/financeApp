from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    db_driver: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

apiSettings = Settings()
dbSettings = Settings()
