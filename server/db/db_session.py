from sqlalchemy import create_engine
import sqlalchemy.orm as orm
import os

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Database file isn't specified!")

    # Get absolute path relative to this file's directory (or project root)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    db_path = os.path.abspath(os.path.join(base_dir, db_file.strip()))

    if not os.path.exists(os.path.dirname(db_path)):
        raise Exception(
            f"Directory for database does not exist: {os.path.dirname(db_path)}"
        )

    connection_string = f"sqlite:///{db_path}?check_same_thread=False"
    print(f"Connecting to the database at {connection_string}")

    engine = create_engine(connection_string, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    global __factory
    return __factory()
