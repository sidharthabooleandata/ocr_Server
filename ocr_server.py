from fastapi import FastAPI, File, UploadFile
import easyocr
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image

app = FastAPI()

# Allow CORS so your Streamlit can access it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

reader = easyocr.Reader(['en'], gpu=False)

@app.post("/parse")
async def parse(file: UploadFile = File(...)):
    content = await file.read()
    img = Image.open(io.BytesIO(content)).convert("RGB")
    result = reader.readtext(img)
    text = " ".join([txt for (_, txt, _) in result])
    return {"text": text}
