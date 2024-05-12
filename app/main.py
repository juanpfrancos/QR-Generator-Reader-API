import base64
import datetime
from io import BytesIO
from fastapi import FastAPI, Header, HTTPException
from PIL import Image
import qrcode
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/qr_code")
async def generate_qr_code(
    username: str = Header(None),
):
    if not username:
        raise HTTPException(status_code=400, detail="Username header is required")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Username: {username}, Timestamp: {datetime.datetime.now().isoformat()}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return {"qr_code_base64": img_base64}