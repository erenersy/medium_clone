from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///./medium.db"

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def veritabanini_olustur():
    SQLModel.metadata.create_all(engine)