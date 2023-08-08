from flask import Flask

app = Flask(__name__)
from routes import *

app.secret_key = "WINDSTYLE"



if __name__ == '__main__':
    app.run(debug=True)