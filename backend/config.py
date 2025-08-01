class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_master.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    RATELIMIT_STORAGE_URL = "redis://localhost:6379"
    # Fla settings
    MIGRATE_DIRECTORY = 'migrations'