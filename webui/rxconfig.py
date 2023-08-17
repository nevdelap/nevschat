import reflex as rx


class WebuiConfig(rx.Config):
    pass


config = WebuiConfig(
    app_name="webui",
    api_url="http://nevdelap.com:8000",
    db_url="sqlite:///reflex.db",
    frontend_packages=[
        "react-loading-icons",
    ],
)
