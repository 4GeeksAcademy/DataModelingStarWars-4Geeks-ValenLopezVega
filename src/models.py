from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(130), nullable=False)

    fav_chars: Mapped[List['FavoriteCharacter']] = relationship(back_populates='char_user')
    fav_planets: Mapped[List['FavoritePlanet']] = relationship(back_populates='planet_user')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    __tablename__= 'character'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(10))
    home_world_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))

    char_favorite: Mapped[List['FavoriteCharacter']] = relationship(back_populates='character')
    home_world: Mapped['Planet'] = relationship()

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'home_world_name': self.home_world.name if self.home_world else None
        }

class FavoriteCharacter(db.Model):
    __tablename__= 'favorite_character'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), primary_key=True)

    char_user: Mapped['User'] = relationship(back_populates='fav_chars')
    character: Mapped['Character'] = relationship(back_populates='char_favorite')

    def serialize(self):
        return{
            'user_id': self.user_id,
            'character_id': self.character_id
        }

class Planet(db.Model):
    __tablename__= 'planet'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    population: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    climate: Mapped[str] = mapped_column(String(50))

    planet_favorite: Mapped[List['FavoritePlanet']] = relationship(back_populates='planet')

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'terrain': self.terrain,
            'climate': self.climate
        }
    
class FavoritePlanet(db.Model):
    __tablename__= 'favorite_planet'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), primary_key=True)

    planet_user: Mapped['User'] = relationship(back_populates='fav_planets')
    planet: Mapped['Planet'] = relationship(back_populates='planet_favorite')

    def serialize(self):
        return{
            'user_id': self.user_id,
            'planet_id': self.planet_id
        }

