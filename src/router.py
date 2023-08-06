from fastapi import APIRouter
from .config.database import engine
from .locations import crud as locations_crud
from .donations import crud as donations_crud
from .app_suggestions import crud as app_suggestions_crud
from .milkbank import crud as milkbanks_crud
from .users import crud as users_crud
from .auth import crud as auth_crud
from .post_comment import crud as post_comments_crud
from .post_categories import crud as post_categories_crud
from .post import crud as posts_crud
from .question_to_expert import crud as question_to_expert_crud
from fastapi import Depends


router = APIRouter()

router.include_router(auth_crud.router)
router.include_router(
    locations_crud.router, dependencies=[Depends(auth_crud.get_current_user)])
router.include_router(donations_crud.router)
router.include_router(app_suggestions_crud.router)
router.include_router(milkbanks_crud.router)
router.include_router(users_crud.router)
router.include_router(post_comments_crud.router)
router.include_router(posts_crud.router)
router.include_router(question_to_expert_crud.router)
router.include_router(post_categories_crud.router)
