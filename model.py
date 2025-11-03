
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey, Float, DECIMAL, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"


class VehicleType(str, enum.Enum):
    two_wheeler = "two_wheeler"
    three_wheeler = "three_wheeler"
    four_wheeler = "four_wheeler"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole), nullable=False  ,  default=UserRole.customer)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicles = relationship("Vehicle", back_populates="owner")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    is_ev = Column(Boolean , default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plate_number = Column(String, unique=True, index=True)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="vehicles")
    transactions = relationship("ParkingTransaction", back_populates="vehicle")


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_type = Column(Enum(VehicleType), nullable=False)
    is_occupied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_ev = Column(Boolean , default=False)
    transactions = relationship("ParkingTransaction", back_populates="slot")


class ParkingTransaction(Base):
    __tablename__ = "parking_transactions"

    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("parking_slots.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    slot = relationship("ParkingSlot", back_populates="transactions")
    vehicle = relationship("Vehicle", back_populates="transactions")
    payment = relationship("Payment", back_populates="transaction", uselist=False)


class ParkingRate(Base):
    __tablename__ = "parking_rates"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    hourly_rate = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("parking_transactions.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(20), default="pending")
    gateway_order_id = Column(String(100))
    gateway_payment_id = Column(String(100))
    gateway_signature = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime)
    remarks = Column(Text)
    transaction = relationship("ParkingTransaction", back_populates="payment")




