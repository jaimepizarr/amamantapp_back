from fastapi import APIRouter
from .config.database import engine
from .locations import crud as locations_crud
from .donations import crud as donations_crud
from .app_suggestions import crud as app_suggestions_crud
from .milkbank import crud as milkbanks_crud
from .users import crud as users_crud
from .auth import crud as auth_crud
from .post_comment import crud as post_comments_crud
from .post import crud as posts_crud
from fastapi import Depends


router = APIRouter()

router.include_router(auth_crud.router)
router.include_router(
    locations_crud.router)
router.include_router(donations_crud.router)
router.include_router(app_suggestions_crud.router)
router.include_router(milkbanks_crud.router)
router.include_router(users_crud.router)
router.include_router(post_comments_crud.router)
router.include_router(posts_crud.router)


# CRUD para el modelo User

# CRUD para el modelo MilkBank

# CRUD para el modelo Donation

# CRUD para el modelo AppSuggestions

# CRUD para el modelo PostComment

# CRUD para el modelo Post

# CRUD para el modelo PostFile

# CRUD para el modelo PostLike
