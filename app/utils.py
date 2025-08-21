from bson import ObjectId

def to_object_id(id_str: str) -> ObjectId:
    if not ObjectId.is_valid(id_str):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id_str)

def serialize_doc(doc: dict) -> dict:
    """Convierte _id -> id (str) para respuestas JSON limpias."""
    if not doc:
        return doc
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc
