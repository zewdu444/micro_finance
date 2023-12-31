from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
import models.member as Member_models
import models.user as User_models
import models.loan as Loan_models
import schemas.loan as Loan_schemas
from database import get_db, engine
from sqlalchemy.orm import Session, Query, subqueryload
from sqlalchemy import  or_
import datetime, os, shutil, uuid
from typing import Optional
from .auth import get_current_user, get_user_exception
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
from utils.loan_calculator import loan_calculator
from utils.fileupload import store_file
from utils.email import loan_registration_mail
from schemas.email import LoanRequestSchema

router = APIRouter(prefix="/loans", tags=["loans"], responses={404: {"description": "Not found"}})
Loan_models.Base.metadata.create_all(bind=engine)

#  get all loans
@router.get("/", response_model= list[Loan_schemas.LoanApplication])
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
    # add code here to display nested loans, members, users
    member_creater= []
    member_updater = []
    for loan in loans:
         loan.member_id = db.query(Member_models.Members).get(loan.member_id)
         member_creater.append(loan.member_id.created_by)
         member_updater.append(loan.member_id.updated_by)
         loan.created_by = db.query(User_models.Users).get(loan.created_by)
         loan.updated_by = db.query(User_models.Users).get(loan.updated_by)
    for loan, member in zip(loans, member_creater):
         loan.member_id.created_by = db.query(User_models.Users).get(member)
    for loan, member in zip(loans, member_updater):
          loan.member_id.updated_by = db.query(User_models.Users).get(member)
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

# new loan application
@router.post("/")
async def create_loan_application(loan: Loan_schemas.LoanApplicationCreate,
                                  db: Session = Depends(get_db),
                                  login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    new_loan = Loan_models.Loan_applications(**loan.dict())
    new_loan.total_to_pay, new_loan.per_month_payment, new_loan.total_interest = loan_calculator(loan.loan_term, loan.requested_amount, loan.interest_rate)
    new_loan.total_remaining = new_loan.total_to_pay - new_loan.total_paid
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

# update loan application
@router.put("/{id}")
async def update_loan_application(id: int, loan: Loan_schemas.LoanApplicationUpdate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    loan_update = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan application not found")
    for var, value in vars(loan).items():
        if value is not None:
            setattr(loan_update, var, value)
    loan_update.updated_by = login_user.user_id
    loan_update.updated_at = datetime.datetime.utcnow()
    db.commit()
    return {"message": "Loan application updated successfully"}

# delete loan application
@router.delete("/{id}")
async def delete_loan_application(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    loan_delete = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan application not found")
    db.delete(loan_delete)
    db.commit()
    return {"message": "Loan application deleted successfully"}

# get loan transactions
@router.get("/{id}/transactions", response_model=list[Loan_schemas.LoanTransaction])
async def get_loan_transactions(id: int, db: Session = Depends(get_db),
                                login_user:dict=Depends(get_current_user),
                                search: Optional[str] = None,
                                transaction_type: Optional[str] = None,
                                sort_by: Optional[str] = None,
                                page_number: Optional[int] = 1,
                                page_size: Optional[int] = 10):
    if login_user is None:
        raise get_user_exception
    loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    query :Query = db.query(Loan_models.Loan_transactions).filter(Loan_models.Loan_transactions.loan_id == id)
    # search
    if search:
        search_term = f"%{search}%"
        search_fields = [
            {
              'or': [
                {'field':'transaction_type', 'op':'ilike', 'value':search_term},
                {'field':'description', 'op':'ilike', 'value':search_term},
                {'field':'source_account', 'op':'ilike', 'value':search_term},
                {'field':'destination_account', 'op':'ilike', 'value':search_term},
               ]
            }
         ]
        query = apply_filters(query, search_fields, search_term)
    # filter by field
    if transaction_type:
        transaction_type_filter = [{'field':'transaction_type', 'op': '==', 'value': transaction_type}, ]
        query = apply_filters(query, transaction_type_filter, transaction_type)
    # order by
    if sort_by:
        sorted_by_fields = [{'field': sort_by, 'direction': 'asc'}]
        query = apply_sort(query, sorted_by_fields)
    # pagination
    query, pagination = apply_pagination(query, page_number=page_number, page_size=page_size)
    transactions = query.all()
    if len(transactions) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    for transaction in transactions:
        transaction.created_by = db.query(User_models.Users).filter(User_models.Users.user_id == transaction.created_by).first()
        transaction.updated_by = db.query(User_models.Users).filter(User_models.Users.user_id == transaction.updated_by).first()
    return transactions

# get loan transaction by id
@router.get("/{id}/transactions/{transaction_id}", response_model=Loan_schemas.LoanTransaction)
async def get_loan_transaction(id: int, transaction_id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    transaction = db.query(Loan_models.Loan_transactions).filter(Loan_models.Loan_transactions.transaction_id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    transaction.created_by = db.query(User_models.Users).filter(User_models.Users.user_id == transaction.created_by).first()
    transaction.updated_by = db.query(User_models.Users).filter(User_models.Users.user_id == transaction.updated_by).first()
    return transaction

# new loan transaction
@router.post("/{id}/transactions")
async def create_loan_transaction(id: int, transaction: Loan_schemas.LoanTransactionCreate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    new_transaction = Loan_models.Loan_transactions(**transaction.dict())
    new_transaction.loan_id = id
    new_transaction.created_by = login_user.user_id
    new_transaction.updated_by = login_user.user_id
    new_transaction.created_at = datetime.datetime.utcnow()
    new_transaction.updated_at = datetime.datetime.utcnow()
    if transaction.transaction_type == "deposit":
        new_transaction.amount = abs(new_transaction.amount)
    elif transaction.transaction_type == "withdraw":
        new_transaction.amount = -1 * abs(new_transaction.amount)
    loan.total_paid += new_transaction.amount
    loan.total_remaining = loan.total_to_pay - loan.total_paid
    loan.updated_by = login_user.user_id
    loan.updated_at = datetime.datetime.utcnow()
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return {"message": "Transaction created successfully"}

# update loan transaction

@router.put("/{id}/transactions/{transaction_id}")
async def update_loan_transaction(id: int, transaction_id: int, transaction: Loan_schemas.LoanTransactionUpdate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
          raise get_user_exception
    loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    transaction_update = db.query(Loan_models.Loan_transactions).filter(Loan_models.Loan_transactions.transaction_id == transaction_id).first()
    if transaction_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    for var, value in vars(transaction).items():
        if value is not None:
            setattr(transaction_update, var, value)
    if transaction_update.transaction_type == "deposit":
        transaction_update.amount = abs(transaction_update.amount)
    elif transaction_update.transaction_type == "withdraw":
        loan.total_paid += transaction_update.amount
        transaction_update.amount = -1 * abs(transaction_update.amount)
    lon.total_paid += transaction_update.amount
    loan.total_remaining = loan.total_to_pay - loan.total_paid
    loan.updated_by = login_user.user_id
    loan.updated_at = datetime.datetime.utcnow()
    transaction_update.updated_by = login_user.user_id
    transaction_update.updated_at = datetime.datetime.utcnow()
    db.commit()
    return {"message": "Transaction updated successfully"}



# delete loan transaction
@router.delete("/{id}/transactions/{transaction_id}")
async def delete_loan_transaction(id: int, transaction_id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    transaction_delete = db.query(Loan_models.Loan_transactions).filter(Loan_models.Loan_transactions.transaction_id == transaction_id).first()
    if transaction_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    if transaction_delete.transaction_type == "deposit":
        loan.total_paid -= transaction_delete.amount
        loan.total_remaining = loan.total_to_pay - loan.total_paid
    elif transaction_delete.transaction_type == "withdraw":
        loan.total_paid += transaction_delete.amount
        loan.total_remaining = loan.total_to_pay - loan.total_paid
    loan.updated_by = login_user.user_id
    loan.updated_at = datetime.datetime.utcnow()
    db.delete(transaction_delete)
    db.commit()
    return {"message": "Transaction deleted successfully"}

# upload loan related document
@router.post("/{id}/upload")
async def upload_loan_related_document(id: int, file: UploadFile = File(...), db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    loan.related_document = store_file(file, "../uploads/loans")
    loan.updated_by = login_user.user_id
    loan.updated_at = datetime.datetime.utcnow()
    db.commit()
    return {"message": "Loan related document uploaded successfully"}

# delete loan related document
@router.delete("/{id}/upload")
async def delete_loan_related_document(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
       if login_user is None:
            raise get_user_exception
       loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
       if loan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
       loan.related_document = None
       loan.updated_by = login_user.user_id
       loan.updated_at = datetime.datetime.utcnow()
       db.commit()
       return {"message": "Loan related document deleted successfully"}

# upload loan transaction related document
@router.post("/{id}/transactions/{transaction_id}/upload")
async def upload_loan_transaction_related_document(id: int, transaction_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
      if login_user is None:
          raise get_user_exception
      loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
      if loan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
      transaction = db.query(Loan_models.Loan_transactions).filter(Loan_models.Loan_transactions.transaction_id == transaction_id).first()
      if transaction is None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
      transaction.related_document = store_file(file, "../uploads/loans")
      transaction.updated_by = login_user.user_id
      transaction.updated_at = datetime.datetime.utcnow()
      db.commit()
      return {"message": "Loan transaction related document uploaded successfully"}

# delete loan transaction related document
@router.delete("/{id}/transactions/{transaction_id}/upload")
async def delete_loan_transaction_related_document(id: int, transaction_id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
         if login_user is None:
                raise get_user_exception
         loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
         if loan is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
         transaction = db.query(Loan_models.Loan_transactions).filter(Loan_models.Loan_transactions.transaction_id == transaction_id).first()
         if transaction is None:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
         transaction.related_document = None
         transaction.updated_by = login_user.user_id
         transaction.updated_at = datetime.datetime.utcnow()
         db.commit()
         return {"message": "Loan transaction related document deleted successfully"}

# send loan application email
@router.post("/{id}/sendemail")
async def send_loan_application_email(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    loan = db.query(Loan_models.Loan_applications).filter(Loan_models.Loan_applications.loan_id == id).first()
    member = db.query(Member_models.Members).filter(Member_models.Members.member_id == loan.member_id).first()
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    loan_application_data ={
       "email": ["zewdu.erkyhun@yandex.com"],
       "subject": "Regarding your loan application with us ",
       "body":{
           "data": {
              "loan_id": loan.loan_id,
              "member_name": member.firstname + " " + member.lastname,
              "member_phone": member.phone,
              "loan_type": loan.loan_type,
              "requested_amount": loan.requested_amount,
              "loan_term": loan.loan_term,
              "interest_rate": loan.interest_rate,
              "total_to_pay": loan.total_to_pay,
              "per_month_payment": loan.per_month_payment,
              "total_interest": loan.total_interest,
              "loan_status": loan.loan_status,
              "total_paid": loan.total_paid,
              "total_remaining": loan.total_remaining
              }
        }
    }
    try:
       await  loan_registration_mail(LoanRequestSchema(**loan_application_data))
       return {"message": "Loan application email sent successfully"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan application email not sent")

