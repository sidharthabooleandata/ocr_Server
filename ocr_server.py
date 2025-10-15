from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import easyocr
from PIL import Image
import io
from pdf2image import convert_from_bytes

app = FastAPI(title="EasyOCR CPU Server")

# Initialize EasyOCR reader (CPU mode)
reader = easyocr.Reader(['en'], gpu=False)

@app.post("/parse")
async def parse_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        extracted_text = ""

        if file.filename.lower().endswith(".pdf"):
            images = convert_from_bytes(file_bytes)
            for img in images:
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")
                result = reader.readtext(img_bytes.getvalue())
                extracted_text += " ".join([t[1] for t in result]) + "\n"
        else:
            img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
            result = reader.readtext(file_bytes)
            extracted_text = " ".join([t[1] for t in result])

        return JSONResponse(content={"text": extracted_text})

    except Exception as e:
        return JSONResponse(content={"text": "", "error": str(e)}, status_code=500)
