from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)

    trackers = relationship("Tracker", back_populates="users")

class Tracker(Base):
    __tablename__ = "trackers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.telegram_id'), nullable=False)
    tracking_code = Column(String, nullable=False, unique=True)
    state_1 = Column(JSON, nullable=True)
    state_2 = Column(JSON, nullable=True)
    state_3 = Column(JSON, nullable=True)
    state_4 = Column(JSON, nullable=True)
    state_5 = Column(JSON, nullable=True)
    state_6 = Column(JSON, nullable=True)

    def most_recent_state(self):
        for state in [self.state_6, self.state_5, self.state_4, self.state_3, self.state_2, self.state_1]:
            if state:
                return state
        return None

    users = relationship("User", back_populates="trackers")

