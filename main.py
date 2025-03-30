from flask import Flask, render_template, request, jsonify
from Dates_And_Times import Dates_Times
from datetime import datetime

app = Flask(__name__)

times = Dates_Times()


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup')
def days_times():

    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int) 

    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year

    button_labels = times.get_available_lables(month=month,year=year)[1]
    return render_template('main.html', buttons=button_labels,month = str(month), year = str(year))

@app.route('/submit', methods=['POST'])
def button_click():
    value = request.form.get('data')

    print(request.form.get('year'))

    return jsonify({"message": f"'{value}' clicked :D"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug=True)