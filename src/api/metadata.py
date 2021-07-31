from typing import List

import jwt
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from src.data import models
from src.data.mongo import UrlDB

router = APIRouter(tags=["metadata"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/user/metadata", response_model=List[models.UrlMetadata])
async def metadata(request: Request, token: str = Depends(oauth2_scheme)):
    database: UrlDB = request.state.db

    jwt_data = jwt.decode(token, request.state.jwt, algorithms=["HS256"])
    user_urls = await database.get_user_urls("user", jwt_data["user"])
    data = await database.get_metadata("metadata", user_urls)
    return data
