from flask import *
from dotenv import load_dotenv
import os, json
from io import BytesIO
from PIL import Image, ImageDraw

load_dotenv()
app = Flask(__name__)

names = {}
with open("names.json", "r") as file:
    names: dict = json.load(file)

def serve_pil_image(pil_img: Image):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/name/")
def nameIndex():
    return redirect(url_for("index"))

@app.route("/name/<name>")
def showName(name: str):
    if name.lower() not in names.keys():
        return render_template("cannotFindName.html", name=name), 404

    return render_template("name.html", name=name)

@app.route("/getCroppedImage/<name>")
def getCroppedImage(name: str):
    if name.lower() not in names.keys():
        return render_template("cannotFindName.html", name=name), 404

    dimensions = names[name.lower()]
    top = dimensions["top"]
    left = dimensions["left"]
    right = left + dimensions["width"]
    bottom = top + dimensions["height"]

    rectPadding = 5

    image = Image.open("gd10.jpg").convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle([left - rectPadding, top - rectPadding, left + dimensions["width"] + rectPadding, top + dimensions["height"] + rectPadding], width=2, outline="red")

    imgPadding = 150
    cropped_image = image.crop((left - imgPadding, top - imgPadding, right + imgPadding, bottom + imgPadding))

    return serve_pil_image(cropped_image)

app.run(debug=os.getenv("DEBUG") == "TRUE", port=os.getenv("PORT"), host="0.0.0.0")
