import os
from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from app.schemas.book import BookDB
from faker import Faker

# 1. Definizione della variabile mancante
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    echo=True
)


def init_database():
    # 2. Ora 'os' è importato correttamente
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)

    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            for i in range(10):
                # 3. BookDB con la 'B' maiuscola e max_value=5 per i voti
                book = BookDB(
                    title=f.sentence(nb_words=5),
                    author=f.name(),
                    review=f.pyint(min_value=1, max_value=5)
                )
                session.add(book)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]