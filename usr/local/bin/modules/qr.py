import qrcode
import base64
from io import BytesIO
import sys

def run(data):
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    sys.stdout.write(f"\033]1337;File=inline=1;width=auto;height=auto;preserveAspectRatio=1:{qr_base64}\a\n")

    # print(f"data:image/png;base64,{qr_base64}")
    # # print("QR code saved at" + name)
    # return(qr_base64)
