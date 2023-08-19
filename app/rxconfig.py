import socket

import reflex as rx

config = rx.Config(  # type: ignore
    app_name="nevschat",
    api_url=(
        "https://nevdelap.com:8000"
        if socket.gethostname() == "droplet"
        else "http://localhost:8000"
    ),
    db_url="sqlite:///reflex.db",
    frontend_packages=[
        "react-loading-icons",
    ],
)
