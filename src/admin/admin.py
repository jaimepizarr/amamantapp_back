#!/usr/bin/env python3
from typing import Any, Dict
from abc import abstractmethod
from jinja2 import Template
from starlette_admin.contrib.sqla import Admin, ModelView
from sqlalchemy import desc, func, select
from starlette.responses import Response
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette_admin import CustomView
from sqlalchemy.orm import Session
from starlette_admin.fields import ImageField, FileField, HasMany
from src.models import (
    User,
    Location,
    MilkBank,
    Donation,
    AppSuggestions,
    PostComment,
    PostLike,
    Section,
    PostAprendeMas,
    PostHome,
    QuestionToExpert,
    PostCategory
)
import base64
from starlette_admin.views import BaseView
from ..config.database import engine
from datetime import datetime
from ..admin.provider import MyAuthProvider
from ..config.firebase import storage
from uuid import uuid4
from starlette_admin import DropDown
from ..config.firestore import add_document, db as firestore


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


class HomeView(CustomView):
    async def render(self, request: Request, templates: Jinja2Templates) -> Response:
        session: Session = request.state.session
        stmt1 = select(PostComment).limit(10).order_by(desc(PostComment.published_at))
        stmt2 = (
            select(User, func.count(PostComment.id).label("cnt"))
            .limit(5)
            .join(PostComment)
            .group_by(User.id)
            .order_by(desc("cnt"))
        )
        posts = session.execute(stmt1).scalars().all()
        users = session.execute(stmt2).scalars().all()
        return templates.TemplateResponse(
            "home.html", {"request": request, "posts": posts, "users": users}
        )


def addImageFirebase(file_data):
    image_name = str(uuid4())
    t = storage.child("images/"+image_name).put(file_data)
    return storage.child(t["name"]).get_url(None)


class MilkBankView(ModelView):
    fields = [
        "id",
        "name",
        "website",
        "phone_number",
        "email",
        ImageField("image", required=False),
         "is_bank",
         "location",
         "image_url"
    ]
    exclude_fields_from_create = ["donations", "image_url"]
    exclude_fields_from_list = ["donations", "image"]

    #Uploud image fireabse to storage get url and save in db
    async def create(self, request, data) -> Any:
        if data["image"] is not None:
            # read file data
            file_data = await data["image"][0].read()
            image_url = addImageFirebase(file_data)
            data["image_url"] = image_url
            data["image"] =[FileField, None]
            for field in self.fields:
               if field.name == "image_url":
                   field.exclude_from_create = False     
        return await super().create(request, data)
    
    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        if data["image"] is not None:
            # read file data
            file_data = await data["image"][0].read()
            image_url = addImageFirebase(file_data)
            data["image_url"] = image_url
            data["image"] =[FileField, None]
            for field in self.fields:
               if field.name == "image_url":
                   field.exclude_from_create = False
        return await super().edit(request, pk, data)


class PostAdminView(ModelView):
    fields = [
        "id",
        "title",
        "section",
        "content",
        ImageField("image", required=False),
        "image_url",
        ]
    exclude_fields_from_create = ["image_url"]
    exclude_fields_from_edit = ["image_url"]
    exclude_fields_from_list = ["image"]

    #Uploud image fireabse to storage get url and save in db
    async def create(self, request, data) -> Any:
        if data["image"] is not None:
            # read file data
            file_data = await data["image"][0].read()
            image_name = str(uuid4())
            t = storage.child("images/"+image_name).put(file_data)
            data["image_url"] = storage.child(t["name"]).get_url(None)
            data["image"] =[FileField, None]
            for field in self.fields:
               if field.name == "image_url":
                   field.exclude_from_create = False     
        return await super().create(request, data)

class PostComentView(ModelView):
    fields = [
        "id",
        "user",
        "content",
        "content",
        "is_commentable",
        "is_likeable",
        "published_at",
        "approved",
        "post_likes",
        "category"
    ]
    
    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        postCommentPrev =  request.state.session.execute(select(PostComment).where(PostComment.id == pk)).scalar_one()
        if postCommentPrev.approved == False and data["approved"] == True:
            user_ref = firestore.document(f"users/{postCommentPrev.user.id}")
            post_firebase = {
                "id": postCommentPrev.id,
                "user_id": postCommentPrev.user.id,
                "user": user_ref,
                "content": postCommentPrev.content,
                "categories": [postCommentPrev.category.name, "Todos" ],
            }
            add_document("posts", pk, post_firebase)
            
        return await super().edit(request, pk, data)


def add_views_to_app(app, engine_db):
    admin = Admin(
        engine_db,
        title="AmamantApp API",
        index_view=HomeView(label="Home", icon="fa fa-home"),
        auth_provider=MyAuthProvider(),
    )
    admin.add_view(DropDown(
        "Users",
        icon="fa fa-user",
        views=[
            ModelView(User, icon="fa fa-user"),
            ModelView(Donation, icon="fa fa-gift")
        ]

    ))
 
    admin.add_view(DropDown(
        "Locations",
        icon="fa fa-map-marker",
        views=[
            MilkBankView(MilkBank, icon="fa fa-building"),
            ModelView(Location, icon="fa fa-map-marker"),
        ]
    ))
  
    admin.add_view(DropDown
                   ("Comunity",
                    icon="fa fa-users",
                    views=[
                        ModelView(PostCategory, name= "Post Categories", label="Post Categories" ,icon="fa fa-tags"),
                        PostComentView(PostComment, icon="fa fa-comment"),
                        ModelView(PostLike, icon="fa fa-thumbs-up"),

                    ]))
    admin.add_view(ModelView(AppSuggestions, icon="fa fa-comment"))

    admin.add_view(
        DropDown(
        "Posts",
        icon="fa fa-newspaper",
        views=[
            ModelView(Section, icon="fa fa-newspaper-o"),
            PostAdminView(PostHome, icon="fa fa-newspaper-o"),
            PostAdminView(PostAprendeMas, icon="fa fa-newspaper-o"),
           
        ]
        
        )
    )
    admin.add_view(ModelView(QuestionToExpert, icon="fa fa-question"))


    admin.mount_to(app)

    return app
