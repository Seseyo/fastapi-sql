from sqlalchemy import Column, Integer, String, Float, ForeignKey

from db.config import Base


class Dish(Base):
    __tablename__ = "dish"
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(128))
    price = Column(Float)
    submenu_id = Column(Integer, ForeignKey('submenu.id'))

    def __repr__(self):
        return '<Dish id: {}, title: {}, description: {}, price: {}, submenu_id: {}>'.format(
            self.id,
            self.title,
            self.description,
            self.price,
            self.menu_id
            )
