#!/usr/bin/env python3
from jinja2 import Template
from starlette_admin.contrib.sqla import Admin, ModelView
from sqlalchemy import desc, func, select
from starlette.responses import Response
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette_admin import CustomView
from sqlalchemy.orm import Session
from src.models import (
    User,
    Location,
    MilkBank,
    Donation,
    AppSuggestions,
    PostComment,
    PostLike,
)


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
    admin.add_view(ModelView(PostComment, icon="fa fa-comment"))
    admin.mount_to(app)

    return app
