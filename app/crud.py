from sqlalchemy.orm import session
from models import Channel

def get_channels(db: session):
    return db.query(Channel).all()

def create_channel(db: session, name: str, url: str):
    new_channel = Channel(name=name, url=url)
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return new_channel
