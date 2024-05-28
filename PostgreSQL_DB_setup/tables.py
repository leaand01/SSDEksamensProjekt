from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Enum as SQLAlchemyEnum
import enum


Base = declarative_base()


class Calcs(Base):
    __tablename__ = 'calcs'
    calc_id = Column(Integer, primary_key=True)
    house_price = Column(String)
    down_payment = Column(String)
    bond_price = Column(String)
    bank_name = Column(String)
    principal_value = Column(String)
    capital_loss = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))

    user = relationship("Users", back_populates="calcs")
    calcs_shared_with_all_users = relationship("Users",
                                               secondary='sharedCalcsWithAll',
                                               back_populates="users_shared_calcs_to_all")
    calcs_shared_selected_users = relationship("Users",
                                               secondary="sharedCalcsWithFew",
                                               back_populates="users_shared_calcs_to_selected")


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)

    calcs = relationship("Calcs", back_populates="user")
    users_shared_calcs_to_all = relationship("Calcs",
                                             secondary='sharedCalcsWithAll',
                                             back_populates="calcs_shared_with_all_users")
    users_shared_calcs_to_selected = relationship("Calcs",
                                                  secondary="sharedCalcsWithFew",
                                                  back_populates="calcs_shared_selected_users")


class Transform(enum.Enum):
    read_only = 'read_only'
    write = 'write'
    admin = 'admin'

    def __str__(self):
        return self.value


class SharedCalcsWithFew(Base):
    __tablename__ = 'sharedCalcsWithFew'
    shared_id = Column(Integer, primary_key=True)
    calc_id = Column(Integer, ForeignKey('calcs.calc_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))  # user_id who calc is shared with
    access_level = Column(SQLAlchemyEnum(Transform, name="access_level_enum"), default=Transform.read_only)

    __table_args__ = (UniqueConstraint('calc_id', 'user_id', name='unique_calc_user'),)


class SharedCalcsWithAll(Base):
    __tablename__ = 'sharedCalcsWithAll'
    calc_id = Column(Integer, ForeignKey('calcs.calc_id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    access_level = Column(SQLAlchemyEnum(Transform, name="access_level_enum"), default=Transform.read_only)
