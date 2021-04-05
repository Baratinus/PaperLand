from flask import Flask,render_template,request,send_from_directory

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    print(app.config["PATH"])
    return send_from_directory(os.path.join(app.config["PATH"], 'static/img'), 'favicon.ico')

app.run(debug=True, port=app.config["PORT"], host=app.config["IP"])