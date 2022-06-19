import datetime
import io
import numpy as np
import cv2
import imutils
import pytesseract
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def home():
    return render_template("index.html", title="Nhận diện biển số xe")


@app.route('/scanner', methods=['GET', 'POST'])
def scan_file():
    if request.method == 'POST':
        image_data = request.files['file'].read()
        start_time = datetime.datetime.now()

        arr = np.fromstring(image_data, dtype='uint8')
        img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 170, 200)
        (cnts, _) = cv2.findContours(edged.copy(),
                                     cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]

        NumberPlateCnt = None
        count = 0
        for c in cnts:

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)

            if len(approx) == 4:
                NumberPlateCnt = approx
                break
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        new_image = gray[topx:bottomx+1, topy:bottomy+1]

        config = ('-l eng --oem 1 --psm 3')

        scanned_text = pytesseract.image_to_string(new_image, config=config)
        print("Found data:", scanned_text)
        session['data'] = {
            "text": scanned_text,
            "time": str((datetime.datetime.now() - start_time).total_seconds()),
        }
        return redirect(url_for('result'))


@app.route('/result')
def result():
    if "data" in session:
        data = session['data']
        return render_template(
            "result.html",
            title="Kết quả",
            time=data["time"],
            text=data["text"],
            words=len(data["text"].split(" ")),
        )
    else:
        return "Lỗi."


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    app.run(debug=True)
