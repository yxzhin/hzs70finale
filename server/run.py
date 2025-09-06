from server.db import db_session
from server.db.models.__all_models import *
from server.app import create_app


if __name__ == "__main__":
    app = create_app()
    db_session.global_init(app.config.get("DBNAME"))
    app.run(
        debug=True,
        host=app.config.get("HOST"),
        port=app.config.get("PORT"),
    )
