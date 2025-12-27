from sqlalchemy import (
    Column, Integer, Text, String, Boolean, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)


class Coordinator(Base):
    __tablename__ = "coordinators"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Leader(Base):
    __tablename__ = "leader"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # ✅ Nuevo: el líder pertenece a un coordinador
    coordinator_id = Column(Integer, ForeignKey("coordinators.id"), nullable=False)
    coordinator = relationship("Coordinator")


class Municipality(Base):
    __tablename__ = "municipality"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    # ✅ Nuevo: relación formal con department
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    department_rel = relationship("Department")


class Neighborhood(Base):
    __tablename__ = "neighborhood"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    # OJO: en tu DB es id_municipality (no municipality_id)
    id_municipality = Column(Integer, ForeignKey("municipality.id"), nullable=False)
    municipality = relationship("Municipality")


class LoadVoter(Base):
    __tablename__ = "load_voters"
    __table_args__ = (
        UniqueConstraint("document", name="uq_load_voters_document"),
    )

    id = Column(Integer, primary_key=True)
    cluster = Column(Integer, nullable=False, default=1)

    # ✅ Quitamos coordinator del votante: solo leader, y leader ya apunta a coordinator
    id_leader = Column(Integer, ForeignKey("leader.id"), nullable=False)

    document = Column(Text, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)

    id_municipality = Column(Integer, ForeignKey("municipality.id"), nullable=False)
    id_neighborhood = Column(Integer, ForeignKey("neighborhood.id"), nullable=False)

    mode = Column(Text, nullable=False, default="public")

    consent = Column(Boolean, nullable=False)
    consent_at = Column(DateTime(timezone=True), nullable=False)
    consent_ip = Column(Text, nullable=False)
    consent_user_agent = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # ✅ Relaciones válidas (sin Coordinator directo)
    leader = relationship("Leader")
    municipality = relationship("Municipality")
    neighborhood = relationship("Neighborhood")
