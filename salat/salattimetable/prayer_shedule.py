import requests
import datetime
from geopy.geocoders import Nominatim


class PrayerSchedule:
    def __init__(self, city, country):
        # self.prayer_times = {}
        self.city = city
        self.country = country
    
    def get_current_location(self):
        geolocator = Nominatim(user_agent="my_user_agent")
        loc = geolocator.geocode(self.city+','+ self.country)
        print(self.city + " City, " + self.country + " " + "latitude :" ,loc.latitude," longtitude :" ,loc.longitude)
        self.longitude = loc.longitude
        self.latitude = loc.latitude
        return str(loc.latitude) + ":" + str(loc.longitude);

    def make_grid_init(self):
        print("-------------+------------+-------------")
        print("|   Prayer   | Start time |  End time  |")
        print("-------------+------------+-------------")

    def time_func(self, prayer, start, end):
        self.trimmer(prayer,12,1)
        self.trimmer(start,12,0)
        self.trimmer(end,12,2)
        print("-------------+------------+-------------")
        return

    def trimmer(self, word, count, st_flag):
        left_t = int((count - len(word))/2)
        right_t = count - len(word) - left_t
        left_st = left_t * " "
        right_st = right_t * " "
        if(st_flag==1):
            print("|", end='')
        print(left_st + word + right_st + "|", end='')
        if(st_flag==2):
            print("")

    def convert_to_normal_time(self, gmt_time):
        gmt_time = gmt_time.split(" ")[0]
        hour = int(gmt_time.split(":")[0])
        medeterian = "AM"
        if(hour > 12):
            hour = hour - 12
            medeterian = "PM"
        ans = str(hour) + ":" + gmt_time.split(":")[1] + " " + medeterian
        return ans
    

    def set_up_schedule(self):
        location = self.get_current_location()
        latitude = location.split(":")[0] # "35.6840574" 
        # latitude = "35.6840574" 
        longitude = location.split(":")[1] 
        # longitude =  "139.7744912"
        date_now = datetime.datetime.now()
        day = int(date_now.day) - 1
        self.dateDay = day
        # print("day " + str(day))
        year = str(date_now.year)
        self.year = year
        month = str(date_now.month)
        self.month = month
        self.time_chart_start = {}
        self.time_chart_end = {}
        url = "http://api.aladhan.com/v1/calendar/"+year+"/"+month+"?latitude="+latitude+"&longitude="+longitude+"&method=2" # "https://dailyprayer.abdulrcs.repl.co/api/singapore"
        hanafi_api = "https://www.islamicfinder.us/index.php/api/prayer_times?country=BD&zipcode=1230" # https://www.islamicfinder.us/index.php/api/prayer_times?country=JP&zipcode=171-0051
        # https://www.islamicfinder.us/index.php/api/prayer_times?latitude=23.7644025&longitude=90.389015&timezone=Asia/Dhaka
        # print(url)
        response = requests.get(url)
        if(response != None):
            response.raise_for_status()  # raises exception when not a 2xx response
            if response.status_code != 204:
                alldata = response.json()
                data = alldata['data']
                timing = data[day]['timings']
                # print(data[day]['date']['gregorian']['weekday']['en'])
                self.day = data[day]['date']['gregorian']['weekday']['en']
                # print("Prayer time today for date("+ str(date_now).split(" ")[0] + "):\n")
                self.date = date_now.strftime("%B %d, %Y") # str(date_now).split(" ")[0]
                for prayer in timing:
                    gmt_time = timing[prayer]
                    time_medit = self.convert_to_normal_time(gmt_time)
                    # print(prayer + " " + time_medit)
                    self.time_chart_start[prayer] = time_medit
                self.time_chart_end["Fajr"] = self.time_chart_start["Sunrise"]
                self.time_chart_end["Dhuhr"] = self.time_chart_start["Asr"]
                self.time_chart_end["Asr"] = self.time_chart_start["Maghrib"]
                self.time_chart_end["Maghrib"] = self.time_chart_start["Isha"]
                self.time_chart_end["Isha"] = self.time_chart_start["Imsak"]

    def print_up_schedule(self):
        self.set_up_schedule()
        self.make_grid_init()
        self.time_func("Fajr", self.time_chart_start["Fajr"], self.time_chart_end["Fajr"])
        self.time_func("Dhuhr", self.time_chart_start["Dhuhr"], self.time_chart_end["Dhuhr"])
        self.time_func("Asr", self.time_chart_start["Asr"], self.time_chart_end["Asr"])
        self.time_func("Maghrib", self.time_chart_start["Maghrib"], self.time_chart_end["Maghrib"])
        self.time_func("Isha", self.time_chart_start["Isha"], self.time_chart_end["Isha"])
        # time_chart_start[prayer]
        self.time_func("Midnight", self.time_chart_start["Midnight"], "-")
        self.time_func("Firstthird", self.time_chart_start["Firstthird"], "-")
        self.time_func("Lastthird", self.time_chart_start["Lastthird"], "-")


if __name__ == "__main__":
    # schedule = PrayerSchedule("Dhaka", "Bangladesh") 
    schedule = PrayerSchedule("Tokyo", "Japan") 
    schedule.set_up_schedule()
    print(schedule.time_chart_start)
    print(schedule.time_chart_end)    