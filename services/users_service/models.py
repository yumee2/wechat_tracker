from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
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
    user_id = Column(String, ForeignKey('users.telegram_id'), nullable=False, unique=True)
    tracking_code = Column(String, nullable=False, unique=True)
    state_1 = Column(String, nullable=True)
    state_2 = Column(String, nullable=True)
    state_3 = Column(String, nullable=True)
    state_4 = Column(String, nullable=True)
    state_5 = Column(String, nullable=True)
    state_6 = Column(String, nullable=True)

    def most_recent_state(self) -> str | None:
        for state in reversed([
            self.state_1,
            self.state_2,
            self.state_3,
            self.state_4,
            self.state_5,
            self.state_6,
        ]):
            if state is not None:
                return state
        return None

    users = relationship("User", back_populates="trackers")