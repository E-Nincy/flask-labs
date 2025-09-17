from flask import Flask

app = Flask(__name__)


@app.route('/')
def welcome():
    return "Welcome to Emily's Dog Costumes!"


@app.route('/services')
def services():
    page = "I offer custom made costumes for your precious canine companion, "\
        "and a free in-home consultation, to get the measurements."


@app.route('/costumes/costume')
def costumes(costume):
    return f"Check out this {costume} costume!"

if __name__ == '__main__':
    app.run(debug=True)
