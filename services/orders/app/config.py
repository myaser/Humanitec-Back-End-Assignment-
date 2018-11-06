from flask_env import MetaFlaskEnv


class BaseConfig(metaclass=MetaFlaskEnv):
    """Base configuration"""
    DEBUG = False
    TESTING = False

    JWT_HEADER_NAME = None
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ALGORITHM = 'RS256'
    JWT_SECRET_KEY = None
    JWT_PUBLIC_KEY = None
    JWT_PRIVATE_KEY = None
    JWT_DECODE_AUDIENCE = None
    RESTPLUS_MASK_SWAGGER = False

    # USERS_SERVICE_URL = os.environ.get('USERS_SERVICE_URL')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


class StagingConfig(BaseConfig):
    """Staging configuration"""
    DEBUG = False


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
