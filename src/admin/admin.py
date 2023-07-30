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
    PostFile,
    Section,
    PostAprendeMas,
    PostHome
)
import base64
from starlette_admin.views import BaseView
from ..config.database import engine
from datetime import datetime
from ..admin.provider import MyAuthProvider
from ..config.firebase import storage
from uuid import uuid4
from starlette_admin import DropDown

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


# imagefiled


class PostCommentView(ModelView):
    fields = [
        "id",
        "title",
        "content",
        ImageField("image", required=False),
        "post_files",
        "user",
    ]
    exclude_fields_from_create = ["post_files"]
    exclude_fields_from_list = ["image"]

    async def create(self, request, data) -> Any:
        if data["image"] is not None:
            # read file data
            file_data = await data["image"][0].read()
            # encode data
            data["image"] = base64.b64encode(file_data)
        db = request.state.session
        post_file = PostFile(image=data["image"])
        db.add(post_file)
        db.commit()
        db.refresh(post_file)
        data["post_files"] = [post_file.id]
        data["image"] = [FileField, None]
        for field in self.fields:
            if isinstance(field, HasMany):
                field.exclude_from_create = False

        return await super().create(request, data)
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
            image_name = str(uuid4())
            t = storage.child("images/"+image_name).put(file_data)
            print(t)
            print(storage.child(t["name"]).get_url(None)    )
            data["image_url"] = storage.child(t["name"]).get_url(None)
            data["image"] =[FileField, None]
            print(self.fields)
            for field in self.fields:
               if field.name == "image_url":
                   field.exclude_from_create = False     
        return await super().create(request, data)


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
    exclude_fields_from_list = ["image"]

    #Uploud image fireabse to storage get url and save in db
    async def create(self, request, data) -> Any:
        if data["image"] is not None:
            # read file data
            file_data = await data["image"][0].read()
            image_name = str(uuid4())
            t = storage.child("images/"+image_name).put(file_data)
            print(t)
            print(storage.child(t["name"]).get_url(None)    )
            data["image_url"] = storage.child(t["name"]).get_url(None)
            data["image"] =[FileField, None]
            print(self.fields)
            for field in self.fields:
               if field.name == "image_url":
                   field.exclude_from_create = False     
        return await super().create(request, data)
    

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
                        ModelView(PostComment, icon="fa fa-comment"),
                        ModelView(PostLike, icon="fa fa-thumbs-up"),
                        ModelView(PostFile, icon="fa fa-file"),

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


    admin.mount_to(app)

    return app
