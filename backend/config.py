"""
backend/config.py
-----------------
Application settings loaded from environment variables.
All IBM credentials and app configuration are centralised here.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Reads configuration from the .env file (or real environment variables).
    All fields are required in production; defaults are provided only where
    safe for local development.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "backend/.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # IBM watsonx.ai (Granite)
    # ------------------------------------------------------------------
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"

    # Model identifiers — live supported Granite model on watsonx.ai
    granite_model_id: str = "ibm/granite-4-h-small"
    granite_model_fallback: str = "ibm/granite-13b-instruct-v2"

    # ------------------------------------------------------------------
    # IBM Db2 on Cloud
    # ------------------------------------------------------------------
    db2_dsn: str = ""
    db2_user: str = ""
    db2_password: str = ""

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    app_secret_key: str = "fitness-buddy-dev-key"
    cors_origin: str = "http://localhost:5173"
    debug: bool = True

    # Chat history window sent to Granite (keeps token usage low)
    chat_history_window: int = 5

    # ------------------------------------------------------------------
    # Compatibility properties for uppercase access
    # ------------------------------------------------------------------
    @property
    def WATSONX_API_KEY(self) -> str:
        return self.watsonx_api_key

    @property
    def WATSONX_PROJECT_ID(self) -> str:
        return self.watsonx_project_id

    @property
    def WATSONX_URL(self) -> str:
        return self.watsonx_url

    @property
    def WATSONX_MODEL_ID(self) -> str:
        return self.granite_model_id

    @property
    def DB2_DSN(self) -> str:
        return self.db2_dsn

    @property
    def DB2_USER(self) -> str:
        return self.db2_user

    @property
    def DB2_PASSWORD(self) -> str:
        return self.db2_password


# Singleton — import this everywhere instead of instantiating Settings again
settings = Settings()
