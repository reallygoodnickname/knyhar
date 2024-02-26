from pydantic_settings import BaseSettings, SettingsConfigDict

from logging.config import dictConfig

# Log formatting
log_format = '%(asctime)s [%(levelname)s]: %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'

log_level = 'WARN'

# Logging configuration
dictConfig(
    {
        'version': 1,
        'formatters':
        {
            'default':
            {
                'format': log_format,
                'datefmt': date_format
            }
        },
        'handlers':
        {
            'stdout':
            {
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
        },
        'root':
        {
            'level': log_level,
            'handlers': ['stdout']
        }
    }
)


class Settings(BaseSettings):
    """
    Class representing application settings

    Attributes:
        app_name:    Application name
        secret_key:  Secret key
        host:        Address to listen on
        port:        Port to listen on
        max_pass:    Max. password length
        min_pass:    Min. password length

        db_host:     Database host (in format address:port)
        db_dbname:   Database name
        db_username: Database username
        db_password: Database password

        dbms_name:   DBMS name
        dbms_dbapi:  Databas API used for working with DBMS
    """
    model_config = SettingsConfigDict(env_prefix='knyhar_')

    # Application settings
    app_name: str = "knyhar"
    secret_key: str = "changeme"
    host: str = "127.0.0.1"
    port: int = 8080
    max_pass: int = 64
    min_pass: int = 8

    # Database credentials
    db_host: str = "localhost:5432"
    db_name: str = "knyhar"
    db_username: str = ""
    db_password: str = ""

    # Connector details
    dbms_name: str = "postgresql"
    dbms_dbapi: str = "psycopg"
