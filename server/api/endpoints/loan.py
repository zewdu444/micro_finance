from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
import models.member as Member_models
import models.user as User_models
import models.loan as Loan_models
import schemas.loan as Loan_schemas
from database import get_db, engine
from sqlalchemy.orm import Session, Query
from sqlalchemy import  or_
import datetime
import os
import shutil
import uuid
from typing import Optional
from .auth import get_current_user, get_user_exception
# from utils.fileupload import store_picture

router = APIRouter(prefix="/loans", tags=["loans"], responses={404: {"description": "Not found"}})
Member_models.Base.metadata.create_all(bind=engine)

#  get all loans
@router.get("/", response_model=list[Loan_schemas.LoanApplication])
async def get_loans(db: Session = Depends(get_db),
                      login_user:dict=Depends(get_current_user),
                      search: Optional[str] = None,
                      filter_field: Optional[str] = None,
                      order_by: Optional[str] = None,
                      order_desc: Optional[bool] = False):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(Loan_models.Loan_applications)
    # search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(Loan_models.Loan_applications.loan_type.ilike(search_term),
                Loan_models.Loan_applications.loan_status.ilike(search_term),
                Loan_models.Loan_applications.related_document.ilike(search_term),
                )
                )
        try:
            date_search = datetime.datetime.strptime(search, "%Y-%m-%d")
            query = query.filter(
                or_(
                    Loan_models.Loan_applications.created_at >= date_search,
                    Loan_models.Loan_applications.updated_at >= date_search,
                ))
        except ValueError:
            pass
     # filter by field
    if filter_field:
        if filter_field == "loan_type":
            query = query.filter(Loan_models.Loan_applications.loan_type == "personal") or query.filter(Loan_models.Loan_applications.loan_type == "business")
        elif filter_field == "loan_status":
            query = query.filter(Loan_models.Loan_applications.loan_status == "created") or query.filter(Loan_models.Loan_applications.loan_status == "approved") or query.filter(Loan_models.Loan_applications.loan_status == "rejected") or query.filter(Loan_models.Loan_applications.loan_status == "closed")
    # order by
    if order_by:
        column_attr = getattr(Loan_models.Loan_applications, order_by, None)
        if column_attr is not None:
            if order_desc:
                 query = query.order_by(column_attr.desc())
            else:
                 query = query.order_by(column_attr)
    return query.all()
