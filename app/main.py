import base64
import datetime
from io import BytesIO
from fastapi import FastAPI, Header, HTTPException
from PIL import Image
import qrcode


app = FastAPI()

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