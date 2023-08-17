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
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
# from utils.fileupload import store_picture

router = APIRouter(prefix="/loans", tags=["loans"], responses={404: {"description": "Not found"}})
Loan_models.Base.metadata.create_all(bind=engine)

#  get all loans
@router.get("/", response_model=list[Loan_schemas.LoanApplication])
async def get_loans(db: Session = Depends(get_db),
                      login_user:dict=Depends(get_current_user),
                      search: Optional[str] = None,
                      loan_type: Optional[str] = None,
                      loan_status: Optional[str] = None,
                      sort_by: Optional[str] = None,
                      page_number: Optional[int] = 1,
                      page_size: Optional[int] = 10):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(Loan_models.Loan_applications)
    # search
    if search:
      search_term = f"%{search}%"
      search_fields = [
        {
          'or': [
            {'field':'loan_type', 'op':'ilike', 'value':search_term},
            {'field':'loan_status', 'op':'ilike', 'value':search_term},
            {'field':'related_document','op':'ilike', 'value':search_term},
          ],
        }
      ]
      query = apply_filters(query, search_fields, search_term)
    # filter by field
    if loan_type:
      loan_type_filter = [{'field':'loan_type', 'op': '==', 'value': loan_type}, ]
      query = apply_filters(query, loan_type_filter, loan_type)
    if loan_status:
      loan_status_filter = [{'field':'loan_status', 'op': '==', 'value': loan_status}, ]
      query = apply_filters(query, loan_status_filter, loan_status)
    # order by
    if sort_by:
      sorted_by_fields = [{'field': sort_by, 'direction': 'asc'}]
      query = apply_sort(query, sorted_by_fields)
    # pagination
    query, pagination = apply_pagination(query, page_number=page_number, page_size=page_size)
    if len(query.all()) == 0:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No loans found")
    loans = query.all()
    for loan in loans:
        loan.member_id = db.query(Member_models.Members).filter(Member_models.Members.member_id == loan.member_id).first()
        loan.member_id.created_by = db.query(User_models.Users).filter(User_models.Users.user_id == loan.member_id.created_by).first()
        loan.member_id.updated_by = db.query(User_models.Users).filter(User_models.Users.user_id == loan.member_id.updated_by).first()
        loan.created_by = db.query(User_models.Users).filter(User_models.Users.user_id == loan.created_by).first()
        loan.updated_by = db.query(User_models.Users).filter(User_models.Users.user_id == loan.updated_by).first()
    return loans

# get loan by id
@router.get("/{id}", response_model=Loan_schemas.LoanApplication)
async def get_loan(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    loan.member_id = db.query(Member_models.Members).filter(Member_models.Members.member_id == loan.member_id).first()
    loan.member_id.created_by = db.query(User_models.Users).filter(User_models.Users.user_id == loan.member_id.created_by).first()
    loan.member_id.updated_by = db.query(User_models.Users).filter(User_models.Users.user_id == loan.member_id.updated_by).first()
    loan.created_by = db.query(User_models.Users).filter(User_models.Users.user_id == loan.created_by).first()
    loan.updated_by = db.query(User_models.Users).filter(User_models.Users.user_id == loan.updated_by).first()
    return loan

# update new loan application
@router.post("/")
async def create_loan_application(loan: Loan_schemas.LoanApplicationCreate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    new_loan = Loan_models.Loan_applications(**loan.dict())
    new_loan.loan_status = "created"
    new_loan.is_closed = False
    new_loan.created_by = login_user.user_id
    new_loan.updated_by = login_user.user_id
    new_loan.created_at = datetime.datetime.utcnow()
    new_loan.updated_at = datetime.datetime.utcnow()
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return {"message": "Loan application created successfully"}
