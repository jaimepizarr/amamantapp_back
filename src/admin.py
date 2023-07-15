#!/usr/bin/env python3

from starlette_admin.contrib.sqla import Admin, ModelView
from src.models import (
    User,
    Location,
    MilkBank,
    Donation,
    AppSuggestions,
    PostComment,
    PostLike,
)


def add_views_to_app(app, engine_db):
    admin = Admin(engine_db, title="AmamantApp API")
    admin.add_view(ModelView(User, icon="fa fa-user"))
    admin.add_view(ModelView(PostLike, icon="fa fa-thumbs-up"))
    admin.add_view(ModelView(Location, icon="fa fa-map-marker"))
    admin.add_view(ModelView(MilkBank, icon="fa fa-building"))
    admin.add_view(ModelView(Donation, icon="fa fa-gift"))
    admin.add_view(ModelView(AppSuggestions, icon="fa fa-comment"))
    admin.add_view(ModelView(PostComment, icon="fa fa-comment"))
    admin.mount_to(app)

    return app
