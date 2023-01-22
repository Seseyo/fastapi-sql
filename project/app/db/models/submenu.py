from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.config import Base


class Submenu(Base):
    __tablename__ = "submenu"
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(128))
    menu_id = Column(Integer, ForeignKey('menu.id'))
    dishes = relationship('Dish', backref='dish', lazy='dynamic',
                          cascade = "all, delete, delete-orphan" )

    def __repr__(self):
        return '<Submenu id: {}, title: {}, description: {}, menu_id: {}>'.format(
            self.id,
            self.title,
            self.description,
            self.menu_id
            )
