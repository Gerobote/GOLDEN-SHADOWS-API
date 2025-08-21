import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

_client: AsyncIOMotorClient | None = None
_db = None

async def connect_to_mongo():
    global _client, _db
    uri = os.getenv("MONGODB_URI")
    dbname = os.getenv("MONGODB_DB", "golden_shadows")
    if not uri:
        raise RuntimeError("Falta MONGODB_URI en .env")
    _client = AsyncIOMotorClient(uri)
    _db = _client[dbname]

async def close_mongo_connection():
    global _client
    if _client:
        _client.close()

def db():
    """Devuelve el objeto DB actual."""
    global _db
    if _db is None:
        raise RuntimeError("DB no inicializada. ¿Llamaste connect_to_mongo?")
    return _db
