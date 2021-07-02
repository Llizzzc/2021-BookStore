from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine, Integer, Numeric, ForeignKey


# 创建对象的基类:
Base = declarative_base()


# 定义Admin对象:
class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10))
    password = Column(String(12))

    # 转json方法
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 定义User对象:
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(10))
    password = Column(String(12))
    address = relationship("Address")
    order = relationship("Order")

    # 转json方法
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 定义Address对象
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10))
    phone = Column(Integer)
    city = Column(String(10))
    department = Column(String(30))
    houseNumber = Column(String(10))
    user_id = Column(Integer, ForeignKey('users.id'))
    order = relationship("Order")

    # 转json方法
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 定义Shop对象
class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(10))
    sales = Column(Integer)
    expressLimit = Column(Integer)
    expressPrice = Column(Integer)
    slogan = Column(String(10))
    imgUrl = Column(String(30))
    order = relationship("Order")
    book = relationship("Book",
                        secondary="books_shops_config",
                        backref="shop")

    # 转json方法
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 定义Book对象
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tab = Column(String(10))
    name = Column(String(10))
    imgUrl = Column(String(10))

    # 转json方法
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 定义商店书籍多对多关系
class BSconfig(Base):
    __tablename__ = 'books_shops_config'
    shop_id = Column(Integer, ForeignKey('shops.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    stock = Column(Integer)
    sales = Column(Integer)
    price = Column(Numeric(10, 2))
    oldPrice = Column(Numeric(10, 2))

    # 转json方法
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 定义Order对象
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.id'))
    shop_id = Column(Integer, ForeignKey('shops.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    shopName = Column(String(10))
    isCanceled = Column(String(10))
    book = relationship("Book",
                        secondary="products_orders_config",
                        backref="order")

    # 转json方法
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 定义订单书籍多对多关系
class POconfig(Base):
    __tablename__ = 'products_orders_config'
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    book_sales = Column(Integer)

    # 转json方法
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:czly161123@localhost:3306/online_shop')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
