from flask import Flask 
import sys

HOST = None
app = Flask(__name__)

if len(sys.argv)>1 and sys.argv[1] == "prod":
    HOST = '0.0.0.0'

@app.route('/')
def hello():
    return "You've reached the AI for Social Good hackathon app and the server is up and running"



if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=17001, threaded=True)
