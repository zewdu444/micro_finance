from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
import schemas.member as Member_schemas
import models.member as Member_models
from database import get_db, engine
from sqlalchemy.orm import Session, Query
from sqlalchemy import  or_
import datetime
import os
import shutil
import uuid
from typing import Optional
from .auth import get_current_user, get_user_exception
router = APIRouter(prefix="/members", tags=["members"], responses={404: {"description": "Not found"}})
Member_models.Base.metadata.create_all(bind=engine)

#  get all members
@router.get("/", response_model=list[Member_schemas.Member])
async def get_members(db: Session = Depends(get_db),
                       login_user:dict=Depends(get_current_user),
                      search: Optional[str] = None,
                      filter_field: Optional[str] = None,
                      order_by: Optional[str] = None,
                      order_desc: Optional[bool] = False):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(Member_models.Member)
    # search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(Member_models.Member.firstname.ilike(search_term),
                Member_models.Member.lastname.ilike(search_term),
                Member_models.Member.email.ilike(search_term),
                Member_models.Member.phone.ilike(search_term),
                Member_models.Member.role.ilike(search_term),
                )
                )
        try:
            date_search = datetime.datetime.strptime(search, "%Y-%m-%d")
            query = query.filter(
                or_(
                    Member_models.Member.created_at >= date_search,
                    Member_models.Member.updated_at >= date_search,
                ))
        except ValueError:
            pass
     # filter by field
    if filter_field:
        if filter_field == "role":
            query = query.filter(Member_models.Member.role == "admin")
        elif filter_field == "status":
            query = query.filter(Member_models.Member.status == "active")
    # order by
    if order_by:
        column_attr = getattr(Member_models.Member, order_by, None)
        if column_attr is not None:
            if order_desc:
                 query = query.order_by(column_attr.desc())
            else:
                query = query.order_by(column_attr.asc())
    members = query.all()
    return members

