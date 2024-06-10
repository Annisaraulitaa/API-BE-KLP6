from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

@dataclass
class Admin(db.Model):
    id = db.Column(db.Text(), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    updated_at = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Float, nullable=False)

    def __repr(self) -> str:
        return f"<Admin {self.username}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "updated_at": self.updated_at,
            "created_at": self.created_at
        }

@dataclass
class User(db.Model):
    id = db.Column(db.Text(), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)
    photo_url = db.Column(db.String(100), unique=True, nullable=True)
    role_id = db.Column(db.Text(), nullable=True)
    role_text = db.Column(db.String(100), nullable=True)
    # add foreign key 'created_by' to Admin
    created_by = db.Column(db.Text(), db.ForeignKey('admin.id'), nullable=False)
    updated_at = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Float, nullable=False)

    def __repr(self) -> str:
        return f"<User {self.username}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "photo_url": self.photo_url,
            "role_id": self.role_id,
            "role_text": self.role_text,
            "updated_at": self.updated_at,
            "created_at": self.created_at
        }

@dataclass
class News(db.Model):
    id = db.Column(db.Text(), primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text(), nullable=False)
    photo_url = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Text(), db.ForeignKey('admin.id'), nullable=False)
    updated_at = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Float, nullable=False)

    def __repr(self) -> str:
        return f"<News {self.title}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "photo_url": self.photo_url,
            "updated_at": self.updated_at,
            "created_at": self.created_at
        }

@dataclass
class Event(db.Model):
    id = db.Column(db.Text(), primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text(), nullable=False)
    photo_url = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Text(), db.ForeignKey('admin.id'), nullable=False)
    updated_at = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Float, nullable=False)

    def __repr(self) -> str:
        return f"<Event {self.title}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "photo_url": self.photo_url,
            "updated_at": self.updated_at,
            "created_at": self.created_at
        }

@dataclass
class AchievementCountry(db.Model):
    id: str = db.Column(db.Text(), primary_key=True)
    country: str = db.Column(db.String(100), unique=True, nullable=False)
    title: str = db.Column(db.String(100), unique=True, nullable=False)
    updated_at: float = db.Column(db.Float, nullable=False)
    created_at: float = db.Column(db.Float, nullable=False)
    achievement_id: str = db.Column(db.Text(), db.ForeignKey('achievement.id'), nullable=False)

    achievement = db.relationship('Achievement', back_populates='countries')

    def __repr(self) -> str:
        return f"<AchievementCountry {self.country}>"
    
    def to_dict(self):
        return {
            "country": self.country,
            "title": self.title,
        }

@dataclass
class Achievement(db.Model):
    id: str = db.Column(db.Text(), primary_key=True)
    content: str = db.Column(db.Text(), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    photo_url: str = db.Column(db.String(100), unique=True, nullable=False)
    created_by: str = db.Column(db.Text(), db.ForeignKey('admin.id'), nullable=False)
    updated_at: float = db.Column(db.Float, nullable=False)
    created_at: float = db.Column(db.Float, nullable=False)

    countries = db.relationship('AchievementCountry', back_populates='achievement', cascade='all, delete-orphan')

    def __repr(self) -> str:
        return f"<Achievement {self.id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "year": self.year,
            "content": self.content,
            "photo_url": self.photo_url,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
            "countries": [country.to_dict() for country in self.countries]
        }

@dataclass
class Gallery(db.Model):
    id: str = db.Column(db.Text(), primary_key=True)
    title: str = db.Column(db.String(100), unique=True, nullable=False)
    photo_url: str = db.Column(db.String(100), unique=True, nullable=False)
    created_by: str = db.Column(db.Text(), db.ForeignKey('admin.id'), nullable=False)
    updated_at: float = db.Column(db.Float, nullable=False)
    created_at: float = db.Column(db.Float, nullable=False)

    def __repr(self) -> str:
        return f"<Gallery {self.title}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "photo_url": self.photo_url,
            "updated_at": self.updated_at,
            "created_at": self.created_at
        }