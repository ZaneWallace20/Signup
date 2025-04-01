import calendar
from datetime import datetime, timedelta
import json
import os
from dateutil.relativedelta import relativedelta

class Dates_Times():

    # in months
    max_future = 0

    DATA_FOLDER = "data"
    
    config_dict = {}

    days = {}

    # setup
    def __init__(self):

        config_path = os.path.join(self.DATA_FOLDER,"config.json")

        with open(config_path, "r") as file:
            self.config_dict = json.load(file)

        self.days = self.config_dict["days"]
        self.max_future = self.config_dict["maxFuture"]


    def _day_to_num(self, day):
        days = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }

        return days[day]
    
    # 1st, 2nd ...
    def add_suffix(self, num):

        if 11 <= num % 100 <= 13:
            suffix = 'th'
        else:
            suffix = {
                1: 'st', 
                2: 'nd', 
                3: 'rd'
                }.get(num % 10, 'th')
            
        return suffix

    def num_to_days(self, num):
        days = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }
        return days[num]

    def num_to_months(self, num):
        months = {
            1: "January", 
            2: "February", 
            3: "March", 
            4: "April",
            5: "May", 
            6: "June", 
            7: "July", 
            8: "August",
            9: "September", 
            10: "October", 
            11: "November", 
            12: "December"
        }

        return months[num]


    # recursive func to go from start to end by delta
    # note delta might change to be in config.json
    def _fill_time_dict(self, start, end, time_array=None, delta=timedelta(minutes=30)):

        # basecase 
        if time_array is None:
            time_array = []
        
        # basecase 
        if start + delta >= end:
            return time_array
        
        new_start = start + delta

        # add on
        time_array.append((start, new_start))

        return self._fill_time_dict(start = new_start, end = end, time_array = time_array, delta = delta)



    # get all avalible times based on a month/year
    def get_available(self, month = datetime.now().month, requested_day = None, year = datetime.now().year):
        now = datetime.now()

        current_date = datetime(now.year, now.month, 1)

        future_date = datetime(year, month, 1)
        
        if current_date + relativedelta(months=self.max_future) < future_date:
            return []

        if current_date > future_date:
            return []

        full_month = calendar.monthcalendar(year, month)

        nums_of_week = [self._day_to_num(i["day"]) for i in self.days]

        available = []

        for week in full_month:
            for day_num, day in enumerate(week):

                if day_num not in nums_of_week:
                    continue
                if day == 0:
                    continue
                if requested_day:
                    if day != requested_day:
                        continue

                day_of_week = self.days[nums_of_week.index(day_num)]
                
                start = day_of_week["startTime"]

                end = day_of_week["endTime"]
                
                temp_dict = {
                    "weekday": day_of_week["day"],
                    "month": month,
                    "year": year,
                    "day":day,
                    "availableTimes":  [] 
                }

                start_time = datetime.strptime(start, "%I:%M %p").replace(year=year, month=month)
                end_time = datetime.strptime(end, "%I:%M %p").replace(year=year, month=month)

                temp_dict["availableTimes"] = self._fill_time_dict(
                    start_time,  
                    end_time
                )

                available.append(temp_dict)
    
        return available

    # get the dates and lables for buttons for main.html
    def get_available_labels(self,month = datetime.now().month, day = datetime.now().day, year = datetime.now().year):
        labels = []

        available = self.get_available(month=month, requested_day=day, year=year)[0]

        array_num = 0

        print(available["availableTimes"])

        for start_time, end_time in available["availableTimes"]:
            

            temp_dict = {
                "title": f"{available["weekday"]}, {self.num_to_months(available["month"])}, {available["day"]}{self.add_suffix(available["day"])}: {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}",
                "number": array_num,
                "day": available["day"],
                "endTime":end_time
            }

            labels.append(temp_dict)

            array_num += 1

        return labels
    
    # get the dates and lables for buttons for main.html
    def get_available_labels_days(self,month = datetime.now().month, year = datetime.now().year):
        labels = []

        print(month, year)

        available = self.get_available(month=month, year=year)

        for i in available:
            temp_dict = {

                "title":  f"{i["weekday"]}, {self.num_to_months(i["month"])}, {i["day"]}{self.add_suffix(i["day"])}",
                "day": i["day"]
                
            }
            labels.append(temp_dict)

        return labels

    def get_days_in_month(self, month = datetime.now().month, year = datetime.now().year):

        mont_stats = calendar.monthrange(year,month)

        temp_dict = {
            "total_days": mont_stats[1],
            "offset": mont_stats[0]
        }

        return temp_dict