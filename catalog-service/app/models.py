from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped,  mapped_column



class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str]
    description: Mapped[str]
    category: Mapped[str]
    image: Mapped[str]
    price: Mapped[int]