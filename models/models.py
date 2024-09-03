from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Boolean, ARRAY, JSON, text
from sqlalchemy.orm import declarative_base, Mapped, DeclarativeMeta
metadata = MetaData()
Base: DeclarativeMeta = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String, nullable=True)
    tel = Column(String, nullable=True)
    address = Column(String, nullable=True)
    orders = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    chatID = Column(String, nullable=True)
    favourites = Column(ARRAY(Integer), nullable=True)
    role = Column(String, nullable=True)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}

class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = Column(Integer, unique=True, primary_key=True)
    number: Mapped[int] = Column(Integer, nullable=True)
    items: Mapped[list] = Column(ARRAY(JSON), nullable=True)
    total: Mapped[int] = Column(Integer, default=0)
    date: Mapped[str] = Column(String, nullable=True)
    address: Mapped[str] = Column(String, nullable=True)
    state: Mapped[str] = Column(String, nullable=True)
    isDelivery: Mapped[bool] = Column(Boolean, default=False)
    payment: Mapped[str] = Column(String, nullable=True)
    comment: Mapped[str] = Column(String, nullable=True)
    client: Mapped[str] = Column(ForeignKey("user.id"), nullable=True)
    cutlery: Mapped[str] = Column(Integer, nullable=True, default=1)


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, unique=True, primary_key=True)
    categoryName = Column(String, nullable=True)
    food = Column(ARRAY(Integer), nullable=True)


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}

class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, unique=True, primary_key=True)
    foodName = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    category = Column(Integer, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}
    
class Promo(Base):
    __tablename__ = "promo"
    id = Column(Integer, unique=True, primary_key=True)
    code = Column(String, nullable=False)
    isPercent = Column(Boolean)
    discount = Column(Integer, nullable=False)
    maxUse = Column(Integer, nullable=False)
    used = Column(ARRAY(Integer), nullable=False)
    desc = Column(String, nullable=True)

# class rating(Base) :
#     __tablename__ = "rating"
#     id = Column(Integer, unique=True, primary_key=True)
#     nickname = Column(String, nullable=True)
#     num = Column(String, nullable=True)
    
    
#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}
