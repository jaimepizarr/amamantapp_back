from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Double
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .config.database import Base
from starlette.requests import Request
import datetime
from sqlalchemy.ext.mutable import MutableDict


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String, index=True)
    longitude = Column(Double, index=True )
    latitude = Column(Double, index=True)
    name = Column(String, index=True)
    users = relationship("User", back_populates="location")
    milk_banks = relationship("MilkBank", back_populates="location")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="NO ACTION"))
    location = relationship("Location", back_populates="users")
    donations_made = relationship(
        "Donation", back_populates="donor", foreign_keys="Donation.user_id"
    )
    donations_approved = relationship(
        "Donation", back_populates="approver", foreign_keys="Donation.approved_by"
    )
    app_suggestions = relationship("AppSuggestions", back_populates="user")
    post_comments = relationship("PostComment", back_populates="user")
    post_likes = relationship("PostLike", back_populates="user")
    surveys = relationship("Survey", back_populates="user")


class MilkBank(Base):
    __tablename__ = "milk_banks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="NO ACTION"))
    website = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=True)
    is_bank = Column(Boolean, default=True, index=True)
    email = Column(String, nullable=True, index=True)
    image_url = Column(String, nullable=True)
    location = relationship("Location", back_populates="milk_banks")
    donations = relationship("Donation", back_populates="bank")


class Donation(Base):
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    bank_id = Column(Integer, ForeignKey("milk_banks.id", ondelete="NO ACTION"))
    donation_date = Column(DateTime, nullable=False)
    approved = Column(Boolean, default=False)
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    donor = relationship(
        "User", back_populates="donations_made", foreign_keys=[user_id]
    )
    approver = relationship(
        "User", back_populates="donations_approved", foreign_keys=[approved_by]
    )
    bank = relationship("MilkBank", back_populates="donations")


class AppSuggestions(Base):
    __tablename__ = "app_suggestions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    suggestion = Column(String, nullable=False)
    user = relationship("User", back_populates="app_suggestions")

class PostCategory(Base):
    __tablename__ = "post_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    posts = relationship("PostComment", back_populates="category")

class PostComment(Base):
    __tablename__ = "post_comments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category_id = Column(Integer, ForeignKey("post_categories.id", ondelete="NO ACTION"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    is_commentable = Column(Boolean, default=False)
    is_likeable = Column(Boolean, default=True)
    published_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    from_expert = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey("post_comments.id", ondelete="NO ACTION"))
    user = relationship("User", back_populates="post_comments")
    approved = Column(Boolean, default=False)
    post_id = Column(Integer, ForeignKey("post_comments.id", ondelete="NO ACTION"))
    post_likes = relationship("PostLike", back_populates="post_comment")
    category = relationship("PostCategory", back_populates="posts")
    image_url = Column(String, nullable=True)
    async def __admin_repr__(self, request: Request):
        return f"{self.title}"


class PostLike(Base):
    __tablename__ = "post_likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    post_id = Column(Integer, ForeignKey("post_comments.id", ondelete="NO ACTION"))
    user = relationship("User", back_populates="post_likes")
    post_comment = relationship("PostComment", back_populates="post_likes")


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    home_posts = relationship("PostHome", back_populates="section")
    aprende_mas_posts = relationship("PostAprendeMas", back_populates="section")

class PostBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"))

class PostHome(PostBase):
    __tablename__ = "home_posts"
    section = relationship("Section", back_populates="home_posts")

class PostAprendeMas(PostBase):
    __tablename__ = "aprende_mas_posts"
    section = relationship("Section", back_populates="aprende_mas_posts")


class QuestionToExpert(Base):
    __tablename__ = "questions_to_experts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=True)


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True, index=True)
    survey = Column(MutableDict.as_mutable(JSONB))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    user = relationship("User", back_populates="surveys")
