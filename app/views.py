from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

app.run(debug=True, port='5000', host='192.168.225.218')