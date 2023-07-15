from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from .config.database import Base


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String, index=True)
    users = relationship("User", back_populates="location")
    milk_banks = relationship("MilkBank", back_populates="location")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
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


class MilkBank(Base):
    __tablename__ = "milk_banks"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="NO ACTION"))
    website = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
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


class PostComment(Base):
    __tablename__ = "post_comments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    is_commentable = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey("post_comments.id", ondelete="NO ACTION"))
    user = relationship("User", back_populates="post_comments")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    user = relationship("User")
    post_files = relationship("PostFile", back_populates="post")
    post_likes = relationship("PostLike", back_populates="post")


class PostFile(Base):
    __tablename__ = "post_files"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="NO ACTION"))
    image = Column(String, nullable=False)
    post = relationship("Post", back_populates="post_files")


class PostLike(Base):
    __tablename__ = "post_likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="NO ACTION"))
    is_likeable = Column(Boolean, default=True)
    user = relationship("User", back_populates="post_likes")
    post = relationship("Post", back_populates="post_likes")