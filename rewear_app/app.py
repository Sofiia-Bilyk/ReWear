from flask import Flask
from models import db

app = Flask(__name__)

#configurations 
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "ReWear backend is running!"


if __name__ == "__main__":
    app.run(debug=True)

