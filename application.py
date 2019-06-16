"""Cloud Foundry test"""
from flask import Flask
import os

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

@app.route('/')
def hello_world():
    return 'Hello world!'

if __name__ == '__main__':
    app.run (port=port)
