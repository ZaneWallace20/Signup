from flask import Flask, render_template, request, jsonify
from Dates_And_Times import Dates_Times
from datetime import datetime

app = Flask(__name__)

times = Dates_Times()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup')
def dates():

    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int) 
    location = request.args.get('location')

    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year

    times.adjust_config_dict(value=location)

    data = times.get_available_labels_days(month=month,year=year)

    month_data = times.get_days_in_month(month=month,year=year)

    return render_template(
        'days.html', 
        buttons=data,
        month = str(month), 
        month_string = times.num_to_months(month), 
        year = str(year),
        total_days = month_data["total_days"],
        offset = month_data["offset"]
        )

@app.route('/signupDay')
def days_times():

    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int) 
    day = request.args.get('day', type=int) 

    location = request.args.get('location')

    times.adjust_config_dict(value=location)

    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year
    if not day:
        day = datetime.now().day

    data = times.get_available_labels(month=month,day=day,year=year)

    return render_template('times.html', buttons=data, month = str(month), month_string = times.num_to_months(month), day = str(day) + times.add_suffix(day), year = str(year))

@app.route('/submit', methods=['POST'])
def reserve():
    
    month = request.form.get("month", type=int)
    day = request.form.get("day", type=int)
    year = request.form.get("year", type=int)
    title = request.form.get("title")
    name = request.form.get("name")
    location = request.form.get('location')


    if not month or not day or not year or not title or not name or not location:
        return jsonify({"message": "Error, please try again later D: (0)"})
    

    
    times.adjust_config_dict(value=location)

    data = times.get_available_labels(month=month,day=day,year=year)
    print(data)

    date = None

    for i in data:
        if title == i["title"]:
            date = i
            break
    
    if not date:
        return jsonify({"message": "Error, please try again later D: (1)"})

    if times.reserve(date, name=name):

        return jsonify({"message": f"{date["title"]} reserved :D"})
    else:
        return jsonify({"message": "Error, please try again later D: (2)"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug=True)