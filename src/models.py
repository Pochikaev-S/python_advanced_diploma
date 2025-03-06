from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker, selectinload, joinedload
from sqlalchemy import create_engine, Column, Integer, Table, ForeignKey, func, ARRAY, and_, select
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

from typing import Optional, List

engine = create_engine("sqlite:///diploma.db", echo=False)
Session = sessionmaker(engine)
session = Session()
Base = declarative_base()


followers = Table(
    "followers",
    Base.metadata,
    Column("one", Integer, ForeignKey("users.id"), primary_key=True),
    Column("two", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    api_key: Mapped[Optional[str]]
    following: Mapped[List["User"]] = relationship(
        secondary=followers,
        primaryjoin=(followers.c.one == id),
        secondaryjoin=(followers.c.two == id),
        back_populates="followers",
    )
    followers: Mapped[List["User"]] = relationship(
        secondary=followers,
        primaryjoin=(followers.c.two == id),
        secondaryjoin=(followers.c.one == id),
        back_populates="following",
    )

    twitters: Mapped[List['Twitt']] = relationship(back_populates='user', cascade='all, delete')
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id, self.name}>"

    @classmethod
    def search_by_id(cls, user_name, user_api_key):
        query = select(User).where(and_(User.name == user_name, User.api_key == user_api_key))
        res = session.execute(query)
        return res.scalar()


    # @classmethod
    # def search_following(cls, user_id):
    #     query = select(User).where(User.following == user_id)
    #     res = session.execute(query)
    #     return res.all()
class Twitt(Base):
    __tablename__ = 'twitts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_create: Mapped[datetime] = mapped_column(server_default=func.now())
    tweet_data: Mapped[str]
    tweet_media_ids: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Integer))
    likes: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Integer))

    user: Mapped['User'] = relationship(back_populates='twitters')


Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)


u1 = User(name="serg", api_key="test")
u2 = User(name="jacob")
u3 = User(name='Лена')
u4 = User(name="victor")


session.add_all([u1, u2, u3])

session.flush()

u1.followers.append(u3)
u1.followers.append(u2)
u3.followers.append(u1)


session.add(u4)
session.commit()

# print(u1)
# print(u1.follower)
# print(u1.following)
print(User.search_by_id('serg', 'test'))
# print(User.search_following(1))