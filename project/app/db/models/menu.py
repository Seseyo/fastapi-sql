from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.config import Base


class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(128))
    submenus = relationship('Submenu', backref='submenu', lazy='dynamic',
                            cascade = "all, delete, delete-orphan" )

    def __repr__(self):
        return '<Menu id: {}, title: {}, description: {}>'.format(
            self.id,
            self.title,
            self.description
            )
