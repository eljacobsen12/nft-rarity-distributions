from random import randrange
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ENGINE_OPTIONS
from flask_app import Job


engine = create_engine(
    SQLALCHEMY_DATABASE_URI, **SQLALCHEMY_ENGINE_OPTIONS
)
Session = sessionmaker(engine)


def find_pending_job():
    with Session.begin() as session:
        queue = session.query(Job).filter_by(state="queued")
        if job := queue.first():
            job.state = "processing"
            return job.slug


def process_job(slug):
    print(f"Processing job: {slug}...", end=" ", flush=True)

    result = randrange(1, 10)
    sleep(result)

    with Session.begin() as session:
        session.query(Job).filter_by(slug=slug).update(
            {"result": result, "state": "completed"}
        )

    print(f"done after {result} seconds!")


if __name__ == "__main__":
    while True:
        if slug := find_pending_job():
            process_job(slug)
        else:
            sleep(1)