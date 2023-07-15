import datetime
from pydantic import BaseModel


class LocationBase(BaseModel):
    country: str
    city: str
    address: str


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    pass


class LocationPartialUpdate(BaseModel):
    country: str = None
    city: str = None
    address: str = None


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class UserBase(UserLogin):
    is_admin: bool


class UserCreate(UserBase):
    location_id: int = None


class UserUpdate(UserBase):
    pass


class UserPartialUpdate(BaseModel):
    email: str = None
    password: str = None
    is_admin: bool = None
    location_id: int = None


class User(UserBase):
    id: int
    location: Location

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    access_token: str
    token_type: str


class UserTokenData(BaseModel):
    email: str | None = None


class MilkBankBase(BaseModel):
    website: str
    phone_number: str
    email: str
    location_id: int


class MilkBankCreate(MilkBankBase):
    pass


class MilkBankUpdate(MilkBankBase):
    pass


class MilkBankPartialUpdate(BaseModel):
    website: str = None
    phone_number: str = None
    email: str = None
    location_id: int = None


class MilkBank(MilkBankBase):
    id: int
    location: Location

    class Config:
        orm_mode = True


class DonationBase(BaseModel):
    donation_date: datetime.datetime
    approved: bool
    approved_by: int


class DonationCreate(DonationBase):
    user_id: int
    bank_id: int


class DonationUpdate(DonationBase):
    pass


class Donation(DonationBase):
    id: int
    donor: User
    approver: User
    bank: MilkBank

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
    user: User

    class Config:
        orm_mode = True


class PostCommentBase(BaseModel):
    is_commentable: bool
    user_id: int
    parent_id: int


class PostCommentCreate(PostCommentBase):
    pass


class PostCommentUpdate(PostCommentBase):
    pass


class PostComment(PostCommentBase):
    id: int
    user: User

    class Config:
        orm_mode = True


class PostCommentPartialUpdate(BaseModel):
    is_commentable: bool = None
    user_id: int = None
    parent_id: int = None


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
    user: User

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
    post: Post

    class Config:
        orm_mode = True


class PostLikeBase(BaseModel):
    user_id: int
    post_id: int
    is_likeable: bool


class PostLikeCreate(PostLikeBase):
    pass


class PostLikeUpdate(PostLikeBase):
    pass


class PostLike(PostLikeBase):
    id: int
    user: User
    post: Post

    class Config:
        orm_mode = True
