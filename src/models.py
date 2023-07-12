#!/usr/bin/env python3



from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
    is_admin = Column(Boolean, default=False)
    location_id = Column(Integer, ForeignKey('locations.id'))
    phone_number = Column(String(20))


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    country = Column(String(50))
    city = Column(String(50))
    address = Column(String(50))


class MilkBank(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    website = Column(String(50))
    phone_number = Column(String(20))
    email = Column(String(50), unique=True)

class AppSugerence(Base):
    __tablename__ = 'sugerences'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    sugerence = Column(String(500))

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(50))
    content = Column(String(500))
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    aproved = Column(Boolean, default=False)
    aproved_by = Column(Integer, ForeignKey('users.id'))


class LikesPost(Base):
    __tablename__ = 'likes_posts'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    like = Column(Boolean, default=True)

class PostComment(Base):
    __tablename__ = 'post_comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    content = Column(String(500))
    is_comment = Column(Boolean, default=False)

class PostFile(Base):
    __tablename__ = 'post_files'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    image_url = Column(String(500))

class Donation(Base):
    __tablename__ = 'donations'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.id'), primary_key=True)
    donation_rate = Column(Integer)
    aproved = Column(Boolean, default=False)
    aproved_by = Column(Integer, ForeignKey('users.id'))
