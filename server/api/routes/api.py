from fastapi import APIRouter
from  endpoints import user, auth, passwordmgt, member

api_router = APIRouter()

api_router.include_router(user.router)
api_router.include_router(auth.router)
api_router.include_router(passwordmgt.router)
api_router.include_router(member.router)

