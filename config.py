import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s: %(message)s"
)


class Settings(BaseSettings):
    DOWNLOAD_DIR: Path = Path("./downloaded")
    CONVERT_DIR: Path = Path("./converted")

    FILES: dict[str, dict[str, str]] = {
        "spn2-api-docs.odt": {
            "url": "https://docs.google.com/document/d/1Nsv52MvSjbLb2PCpHlat0gkzw0EvtSgpKHu4mk0MnrA/export?format=odt"
        },
        "spn2-change-log.odt": {
            "url": "https://docs.google.com/document/d/19RJsRncGUw2qHqGGg9lqYZYf7KKXMDL1Mro5o1Qw6QI/export?format=odt"
        },
    }

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
