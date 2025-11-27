from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

if os.environ.get("PRODUCTION") != "true":
    load_dotenv(".env.development")

DATABASE_URL = os.environ.get("DATABASE_URL")
Base = declarative_base()

# ============================================================
#                      ACCOUNT
# ============================================================

class Account(Base):
    __tablename__ = "account"

    id_account = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(128), nullable=False)    
    created_at = Column(DateTime, nullable=False)

    # Relations
    conversations = relationship("Conversation", back_populates="account")


# ============================================================
#                    CONVERSATION
# ============================================================

class Conversation(Base):
    __tablename__ = "conversation"

    id_conversation = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    id_account = Column(Integer, ForeignKey("account.id_account"), nullable=False)

    # Relations
    account = relationship("Account", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

    def to_dict(self):
        return {
            "id": self.id_conversation,
            "title": self.name,
            "timestamp": self.updated_at.isoformat(),
            "messages": [message.content for message in self.messages]
        }


# ============================================================
#                        MESSAGE
# ============================================================

class Message(Base):
    __tablename__ = "message"

    id_message = Column(Integer, primary_key=True)
    content = Column(String(300), nullable=False)
    id_conversation = Column(Integer, ForeignKey("conversation.id_conversation"), nullable=False)

    # Relations
    conversation = relationship("Conversation", back_populates="messages")


# ============================================================
#                        SOURCE
# ============================================================

class Source(Base):
    __tablename__ = "source"

    id_source = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Relations
    guides = relationship("Guide", back_populates="source")


# ============================================================
#                        GUIDE
# ============================================================

class Guide(Base):
    __tablename__ = "guide"

    id_guide = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(6000))
    level = Column(String(20))
    id_source = Column(Integer, ForeignKey("source.id_source"), nullable=False)

    # Relations
    source = relationship("Source", back_populates="guides")
    tags = relationship("Tag", secondary="possess", back_populates="guides")

    def to_dict(self):
        return {
            "id_guide": self.id_guide,
            "title": self.title,
            "content": self.content,
            "level": self.level,
            "source": self.source.name if self.source else None,
            "tags": [tag.name for tag in self.tags]
        }


# ============================================================
#                         TAG
# ============================================================

class Tag(Base):
    __tablename__ = "tag"

    id_tag = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Relations
    guides = relationship("Guide", secondary="possess", back_populates="tags")


# ============================================================
#                   POSSESS (association table)
# ============================================================

class Possess(Base):
    __tablename__ = "possess"

    id_guide = Column(Integer, ForeignKey("guide.id_guide"), primary_key=True)
    id_tag = Column(Integer, ForeignKey("tag.id_tag"), primary_key=True)


# ============================================================
#           ENGINE + CREATION DES TABLES + SESSION
# ============================================================

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
