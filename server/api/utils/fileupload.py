import os
import shutil
import uuid

def store_picture(file,path):
    upload_folder =path
    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)
    #get destination path
    dest = os.path.join(upload_folder, f"{uuid.uuid1(clock_seq=1)}{file.filename}")
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return os.path.realpath(dest)

def store_file(file,path):
    upload_folder =path
    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)
    #get destination path
    dest = os.path.join(upload_folder, f"{uuid.uuid1(clock_seq=1)}{file.filename}")
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return os.path.realpath(dest)
