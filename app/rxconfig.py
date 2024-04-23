# mypy: disable-error-code="attr-defined,name-defined"

import socket

import reflex as rx

PROD_HOSTNAMES = [
    "buildkitsandbox",  # Build time docker container.
    "prod",  # Prod runtime docker container.
]

is_prod = socket.gethostname() in PROD_HOSTNAMES
config = rx.Config(
    app_name="nevschat",
    api_url="https://nevdelap.com:8000" if is_prod else "http://localhost:8000",
    db_url="sqlite:///reflex.db",
    frontend_packages=[
        "react-loading-icons",
    ],
    frontend_path="/chat" if is_prod else "",
)
# In dev the assets are served by reflex on port 3000. In prod it is served by Nginx.
site_runtime_assets_url = (
    "https://nevdelap.com/chat" if is_prod else "http://localhost:3000"
)
