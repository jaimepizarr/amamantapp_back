from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from ..config.jwt import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from .. import models
from fastapi.security import OAuth2PasswordBearer
from ..schemas import UserTokenData, UserLogin, UserToken, UserCreate
from ..config.database import engine

router = APIRouter(prefix="/auth", tags=["Authentication"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = UserTokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@router.post("/login", response_model=UserToken)
async def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"email": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/signup", response_model=UserToken)
def signup_for_access_token(user: UserCreate, db: Session = Depends(get_db)):
    user = models.User(email=user.email, password=get_password_hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
