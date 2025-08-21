from fastapi import APIRouter, HTTPException
from typing import List
from app.db import db
from app.schemas import VictimCreate, VictimUpdate, VictimOut
from app.utils import to_object_id, serialize_doc

router = APIRouter()

@router.get("/", response_model=List[VictimOut])
async def list_victims():
    docs = await db().victims.find({}).to_list(length=1000)
    return [serialize_doc(d) for d in docs]

@router.get("/{victim_id}", response_model=VictimOut)
async def get_victim(victim_id: str):
    try:
        _id = to_object_id(victim_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid victim id")
    doc = await db().victims.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Victim not found")
    return serialize_doc(doc)

@router.post("/", response_model=VictimOut, status_code=201)
async def create_victim(payload: VictimCreate):
    # (Opcional) validar que case_ids existan en colección cases, etc.
    result = await db().victims.insert_one(payload.model_dump())
    doc = await db().victims.find_one({"_id": result.inserted_id})
    return serialize_doc(doc)

@router.patch("/{victim_id}", response_model=VictimOut)
async def update_victim(victim_id: str, patch: VictimUpdate):
    try:
        _id = to_object_id(victim_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid victim id")

    changes = {k: v for k, v in patch.model_dump(exclude_unset=True).items()}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")

    res = await db().victims.update_one({"_id": _id}, {"$set": changes})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Victim not found")

    doc = await db().victims.find_one({"_id": _id})
    return serialize_doc(doc)

@router.delete("/{victim_id}", status_code=204)
async def delete_victim(victim_id: str):
    try:
        _id = to_object_id(victim_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid victim id")

    res = await db().victims.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Victim not found")
    return None
