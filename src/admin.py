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
from starlette_admin.fields import ImageField
from src.models import (
    User,
    Location,
    MilkBank,
    Donation,
    AppSuggestions,
    PostComment,
    PostLike,
    PostFile,
)
import base64
from .config.database import engine


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
        "user",
        "title",
        "content",
        "published_at",
        ImageField("image"),
    ]

    async def create(self, request: Request, data: Dict[str, Any]):
        image = data["image"][0]
        data.pop("image")
        content = await image.read()
        base64_data = base64.b64encode(content).decode("utf-8")
        db = next(get_db())
        post_file = PostFile()
        post_file.image = base64_data
        db.add(post_file)
        db.commit()
        db.refresh(post_file)
        data["parent_id"] = None
        data["post_files"] = [post_file.id]
        data["post_likes"] = None
        self.fields.pop()
        self.fields = self.fields + ["post_files", "post_likes", "parent_id"]
        return await super().create(request, data)


def add_views_to_app(app, engine_db):
    admin = Admin(
        engine_db,
        title="AmamantApp API",
        index_view=HomeView(label="Home", icon="fa fa-home"),
    )

    admin.add_view(ModelView(User, icon="fa fa-user"))
    admin.add_view(ModelView(PostLike, icon="fa fa-thumbs-up"))
    admin.add_view(ModelView(Location, icon="fa fa-map-marker"))
    admin.add_view(ModelView(MilkBank, icon="fa fa-building"))
    admin.add_view(ModelView(Donation, icon="fa fa-gift"))
    admin.add_view(ModelView(AppSuggestions, icon="fa fa-comment"))
    admin.add_view(PostCommentView(PostComment, icon="fa fa-comment"))
    admin.add_view(ModelView(PostFile, icon="fa fa-file-image-o"))

    admin.mount_to(app)

    return app
