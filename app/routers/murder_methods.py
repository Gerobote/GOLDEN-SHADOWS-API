from fastapi import APIRouter, HTTPException
from typing import List
from app.db import db
from app.schemas import MurderMethodCreate, MurderMethodUpdate, MurderMethodOut
from app.utils import to_object_id, serialize_doc

router = APIRouter()

@router.get("/", response_model=List[MurderMethodOut])
async def list_murder_methods():
    docs = await db().murder_methods.find({}).to_list(length=1000)
    return [serialize_doc(d) for d in docs]

@router.get("/{method_id}", response_model=MurderMethodOut)
async def get_murder_method(method_id: str):
    try:
        _id = to_object_id(method_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid method id")
    doc = await db().murder_methods.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Murder method not found")
    return serialize_doc(doc)

@router.post("/", response_model=MurderMethodOut, status_code=201)
async def create_murder_method(payload: MurderMethodCreate):
    result = await db().murder_methods.insert_one(payload.model_dump())
    doc = await db().murder_methods.find_one({"_id": result.inserted_id})
    return serialize_doc(doc)

@router.patch("/{method_id}", response_model=MurderMethodOut)
async def update_murder_method(method_id: str, patch: MurderMethodUpdate):
    try:
        _id = to_object_id(method_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid method id")
    changes = {k: v for k, v in patch.model_dump(exclude_unset=True).items()}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")
    res = await db().murder_methods.update_one({"_id": _id}, {"$set": changes})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Murder method not found")
    doc = await db().murder_methods.find_one({"_id": _id})
    return serialize_doc(doc)

@router.delete("/{method_id}", status_code=204)
async def delete_murder_method(method_id: str):
    try:
        _id = to_object_id(method_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid method id")
    res = await db().murder_methods.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Murder method not found")
    return None
