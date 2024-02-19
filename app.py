from flask import Flask, render_template

app = Flask(__name__)

EXPENCES = [
  {
    'Id': 1,
    'title': 'salary',
    'amount': 2000,
    'date': '2024-01-01'
  }
]

@app.route("/")
def hello_world():
    return render_template("login.html", expences=EXPENCES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)