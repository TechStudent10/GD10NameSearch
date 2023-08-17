from flask import *
import json
from io import BytesIO
from PIL import Image, ImageDraw

app = Blueprint("main", __name__, url_prefix="/")

names = {}
with open("names.json", "r", encoding="utf8") as file:
    names: dict = json.load(file)

creditsList = []
with open("credits.txt", "r", encoding="utf8") as file:
    creditsList = file.read().split("\n")

def serve_pil_image(pil_img: Image):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

# yeah I have no clue what to name this
def exitIfNotInFiles(name: str):
    if name.lower() not in names.keys():
        if name.upper() not in creditsList:
            return render_template("cannotFindName.html", name=name), 404
        return render_template("nameInCredits.html", name=name)
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/name/")
def nameIndex():
    return redirect(url_for("main.index"))

@app.route("/name/<name>")
def showName(name: str):
    result = exitIfNotInFiles(name)
    if result: return result

    return render_template("name.html", name=name)

@app.route("/getCroppedImage/<name>")
def getCroppedImage(name: str):
    result = exitIfNotInFiles(name)
    if result: return result

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