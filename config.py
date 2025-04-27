import os

flask_app_config = {
    "debug": os.environ.get("FLUSK_DEBUG_OPTION", True),
    "use_reloader": os.environ.get("FLUSK_RELOADER_OPTION", False),
    "host": os.environ.get("FLASK_HOST", "0.0.0.0"),
    "port": os.environ.get("FLASK_PORT", 5000),
}


class Config:
    # Configurazione generica per l'app Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")
