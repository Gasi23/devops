from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from models import Feedback
from database import Base, engine, SessionLocal
from sqlalchemy.future import select

from pydantic import BaseModel

app = FastAPI()

# CORS para acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FeedbackCreate(BaseModel):
    texto: str

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/feedback")
async def criar_feedback(data: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    feedback = Feedback(texto=data.texto)
    db.add(feedback)
    await db.commit()
    return {"mensagem": "Feedback recebido com sucesso!"}

@app.get("/feedbacks")
async def listar_feedbacks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Feedback))
    feedbacks = result.scalars().all()
    return feedbacks
