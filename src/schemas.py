import datetime
from typing import Any, Dict
from typing import Optional
from pydantic import BaseModel, Json,root_validator

class LocationBase(BaseModel):
    country: Optional[str]
    city: Optional[str]
    address: Optional[str]
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class LocationCreate(LocationBase):
    pass

class LocationUpdate(LocationBase):
    pass

class LocationPartialUpdate(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None

class Location(LocationBase):
    id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: Optional[str]
    password: Optional[str]

class UserBase(UserLogin):
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    nombre: str
    apellido: str

class UserUpdate(UserBase):
    location_id: int = None
    profile_picture: str = None
    pass

class UserPartialUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    location_id: Optional[int] = None
    profile_picture: str = None

class User(UserBase):
    id: int
    location: Optional[Location]

    class Config:
        orm_mode = True

class UserToken(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Optional[str]
    id: Optional[int]

class UserTokenData(BaseModel):
    email: Optional[str] = None

class MilkBankBase(BaseModel):
    name: Optional[str]
    website: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    location_id: Optional[int]
    is_bank: Optional[bool]
    image_url: Optional[str]

class MilkBankCreate(MilkBankBase):
    pass

class MilkBankUpdate(MilkBankBase):
    pass

class MilkBankPartialUpdate(BaseModel):
    website: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    location_id: Optional[int] = None

class MilkBank(MilkBankBase):
    id: int
    location: Optional[Location]

    class Config:
        orm_mode = True

class DonationBase(BaseModel):
    donation_date: datetime.datetime
    bank_id: Optional[int]

    class Config:
        orm_mode = True

class DonationCreate(DonationBase):
    pass

class DonationUpdate(DonationBase):
    pass

class Donation(DonationBase):
    id: int
    user_id: Optional[int]
    approved: Optional[bool] = None
    approved_by: Optional[int] = None
    donor: Optional[User] | None
    bank: Optional[MilkBank] | None

    class Config:
        orm_mode = True

class AppSuggestionsBase(BaseModel):
    suggestion: str
    user_id: int

class AppSuggestionsCreate(AppSuggestionsBase):
    pass

class AppSuggestionsUpdate(AppSuggestionsBase):
    pass

class AppSuggestions(AppSuggestionsBase):
    id: int
    user: Optional[User]

    class Config:
        orm_mode = True


class PostCategoriesBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class PostCategoriesRetrieve(PostCategoriesBase):
    id: int
    class Config:
        orm_mode = True

class PostCommentBase(BaseModel):
    title: Optional[str] = None
    content: str
    is_commentable: Optional[bool] = True
    is_likeable: Optional[bool] = True
    parent_id: Optional[int] = None
    category_id: Optional[int] = None

class PostCommentCreate(PostCommentBase):
    pass

class PostCommentUpdate(PostCommentBase):
    pass

class PostComment(PostCommentBase):
    id: int
    user_id: Optional[int] = None
    user: Optional[User]
    category : Optional[PostCategoriesRetrieve]
    approved: Optional[bool] = None

    class Config:
        orm_mode = True

class PostCommentPartialUpdate(BaseModel):
    is_commentable: Optional[bool] = None
    user_id: Optional[int] = None
    parent_id: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    user: Optional[User]

    class Config:
        orm_mode = True

class PostFileBase(BaseModel):
    image: str
    post_id: int

class PostFileCreate(PostFileBase):
    pass

class PostFileUpdate(PostFileBase):
    pass

class PostFile(PostFileBase):
    id: int
    post: Optional[Post]

    class Config:
        orm_mode = True

class PostLikeBase(BaseModel):
    user_id: int
    post_id: int
    is_likeable: Optional[bool]

class PostLikeCreate(PostLikeBase):
    pass

class PostLikeUpdate(PostLikeBase):
    pass

class PostLike(PostLikeBase):
    id: int
    user: Optional[User]
    post: Optional[Post]

    class Config:
        orm_mode = True



class QuestionToExpertBase(BaseModel):
    content: str
    image_url: Optional[str] = None

class QuestionToExpertCreate(QuestionToExpertBase):
    pass

class QuestionToExpert(QuestionToExpertBase):
    pass

class Survey(BaseModel):
    survey: Dict[Any, Any]