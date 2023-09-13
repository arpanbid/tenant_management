from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route("/")

def index():
    return render_template("Sample.html")

if(__name__=='__main__'):
    app.secret_key = 'secretivekey'
    app.run(debug=True)

