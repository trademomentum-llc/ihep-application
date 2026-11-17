import pytest

from app.core.config import Settings, settings

REQUIRED = {"DATABASE_URL": "postgresql://u:p@db:5432/x", "REDIS_URL": "redis://r:6379/0"}


@pytest.mark.unit
def test_settings_load_required_values_from_environment():
    assert settings.DATABASE_URL.startswith("postgresql://")
    assert settings.REDIS_URL.startswith("redis://")


@pytest.mark.unit
@pytest.mark.parametrize("env", ["development", "test", "staging", "production"])
def test_environment_accepts_known_values(env):
    assert Settings(ENVIRONMENT=env, **REQUIRED).ENVIRONMENT == env


@pytest.mark.unit
def test_environment_rejects_unknown_value():
    with pytest.raises(ValueError, match="ENVIRONMENT must be one of"):
        Settings(ENVIRONMENT="qa", **REQUIRED)


@pytest.mark.unit
def test_allowed_origins_parses_comma_separated_string():
    s = Settings(ALLOWED_ORIGINS="https://a.example, https://b.example", **REQUIRED)
    assert s.ALLOWED_ORIGINS == ["https://a.example", "https://b.example"]


@pytest.mark.unit
def test_secret_key_defaults_to_random_value():
    a, b = Settings(**REQUIRED), Settings(**REQUIRED)
    assert len(a.SECRET_KEY) >= 32 and a.SECRET_KEY != b.SECRET_KEY
