from app.core.settings import settings

print(settings.jwt_secret_key)
print(settings.jwt_algorithm)
print(settings.jwt_access_token_expire_minutes)