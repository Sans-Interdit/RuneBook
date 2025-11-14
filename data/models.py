from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv
import secrets
import hashlib
import datetime

if os.environ.get("PRODUCTION") != "true":
    # En local, charge le fichier .env.development
    load_dotenv(".env.development")

DATABASE_URL = os.environ.get("DATABASE_URL")
Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, nullable=False)
    events_created = Column(Integer, default=0)
    is_admin = Column(Boolean, default=False)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    fcm_token = Column(String(255), nullable=True)
    
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    pw_tokens = relationship("PwToken", back_populates="user", cascade="all, delete-orphan")

    def getPublicData(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "phone": self.phone,
            "created_at": self.created_at.strftime("%d/%m/%Y"),
            "events_created": self.events_created,
            "is_admin": self.is_admin,
            "longitude": self.longitude,
            "latitude": self.latitude,
        }
    
class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    paying = Column(Boolean, default=True, nullable=False)
    price = Column(Float, nullable=True)
    photo = Column(String(255), nullable=True)

    address = Column(String(255), nullable=True)
    postal_code = Column(String(10), nullable=False, index=True)
    commune = Column(String(100), nullable=False, index=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    is_approved = Column(Boolean, default=False, nullable=False)
    is_highlight = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="events")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "event_type": self.event_type,
            "description": self.description,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "paying": self.paying,
            "price": self.price,
            "photo": self.photo,
            "address": self.address,
            "postal_code": self.postal_code,
            "commune": self.commune,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "user_id": self.user_id,
            "is_approved": self.is_approved,
            "is_highlight": self.is_highlight,
        }

class PwToken(Base):
    __tablename__ = "pw_token"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    token = Column(String(128), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="pw_tokens")

    @staticmethod
    def generate_for_user(user_id, db_session):
        """Crée un nouveau jeton sécurisé et le stocke haché."""
        raw_token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        expires_at = datetime.datetime.now() + datetime.timedelta(minutes=30)

        pw_token = PwToken(
            user_id=user_id,
            token=hashed_token,
            expires_at=expires_at,
        )

        db_session.add(pw_token)
        db_session.commit()
        return raw_token


engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()