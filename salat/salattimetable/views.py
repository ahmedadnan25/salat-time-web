from django.shortcuts import render
from .models import Task
from .prayer_shedule import PrayerSchedule


def home(request):
    tasks = Task.objects.all()
    schedule = PrayerSchedule("Tokyo", "Japan") 
    schedule.set_up_schedule()
    # print(schedule.time_chart_start)
    # print(schedule.time_chart_end)
    # print(schedule.time_chart_end["Fajr"])
    # print(schedule.date)
    # print(schedule.day)
    timeTable = [
         { "prayer": "Fajr", "starttime" : schedule.time_chart_start["Fajr"], "endtime" : schedule.time_chart_end["Fajr"] },
         { "prayer": "Dhuhr", "starttime" : schedule.time_chart_start["Dhuhr"], "endtime" : schedule.time_chart_end["Dhuhr"] },
         { "prayer": "Asr", "starttime" : schedule.time_chart_start["Asr"], "endtime" : schedule.time_chart_end["Asr"] },
         { "prayer": "Maghrib", "starttime" : schedule.time_chart_start["Maghrib"], "endtime" : schedule.time_chart_end["Maghrib"] },
         { "prayer": "Isha", "starttime" : schedule.time_chart_start["Isha"], "endtime" : schedule.time_chart_end["Isha"] },
    ]
    
    return render(request, 'home.html', {
        'timeTable': timeTable,
        'date' : schedule.date,
        'day' : schedule.day,
    })


# Create your views here.
