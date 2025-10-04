from telegram import Bot, InputFile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import io

app = FastAPI()
bot = Bot(token='ВАШ_ТОКЕН_БОТА')

class PhotoRequest(BaseModel):
    chat_id: int
    photo: str
    filename: str

@app.post("/api/send-photo")
async def send_photo(data: PhotoRequest):
    try:
        photo_bytes = base64.b64decode(data.photo)
        bio = io.BytesIO(photo_bytes)
        bio.name = data.filename
        bio.seek(0)
        await bot.send_photo(chat_id=data.chat_id, photo=InputFile(bio))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
