from flask import *
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    
    from mainBlueprint import app as mainBlueprint
    app.register_blueprint(mainBlueprint)

    return app

if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    app.run(debug=os.getenv("DEBUG") == "TRUE", port=os.getenv("PORT"), host="0.0.0.0")
