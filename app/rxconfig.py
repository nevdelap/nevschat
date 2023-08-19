import reflex as rx


class WebuiConfig(rx.Config):
    pass


config = WebuiConfig(
    app_name="nevschat",
    api_url="http://localhost:8000",
    db_url="sqlite:///reflex.db",
    frontend_packages=[
        "react-loading-icons",
    ],
)
