import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import pylab as pltt
import datetime
import matplotlib.dates as mdates


dict_with_data = {datetime.datetime(2020, 12, 7, 1): 53,
               datetime.datetime(2020, 12, 7, 2): 14,
               datetime.datetime(2020, 12, 7, 3): 15,
               datetime.datetime(2020, 12, 7, 4): 12,
               datetime.datetime(2020, 12, 7, 5): 35,
               datetime.datetime(2020, 12, 7, 6): 31,
               datetime.datetime(2020, 12, 7, 7): 2}

label_of_image = "zsd"

sample_data = {datetime.datetime(2020, 12, 7): 53,
               datetime.datetime(2020, 12, 8): 14,
               datetime.datetime(2020, 12, 9): 15,
               datetime.datetime(2020, 12, 10): 12,
               datetime.datetime(2020, 12, 11): 35,
               datetime.datetime(2020, 12, 12): 31,
               datetime.datetime(2020, 12, 13): 2}


def create_weekday_image(dict_with_data, label_of_image):
    if len(dict_with_data) > 7:
        return
    day_of_week = [0, 1, 2, 3, 4, 5, 6]
    online_on_this_weekday = [0, 0, 0, 0, 0, 0, 0]
    for date in dict_with_data:
        online_on_this_weekday[date.weekday()] = dict_with_data[date]
    labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pltt.rcParams['figure.figsize'] = 7, 5
    pltt.bar(day_of_week, online_on_this_weekday, align='center')
    pltt.xticks(day_of_week, labels)
    pltt.savefig(label_of_image + '.png')
    pltt.close()


def create_daily_image(dict_with_data, label_of_image):
    day_delta = 0
    prev_key = datetime.datetime.now()
    for key in dict_with_data:
        day_delta = key - prev_key
        prev_key = key
    period = day_delta.total_seconds()
    period = period // 60
    number_of_dots = int(1440 // period)
    y_axis = [0] * int(number_of_dots)
    x_axis = [datetime.datetime(2020, 1, 1, 0, 0, 0) + day_delta * i for i in range(number_of_dots)]
    for key in dict_with_data:
        y_axis[int((key.minute + key.hour * 60) // period)] = dict_with_data[key]
    figure, ax = plt.subplots(figsize=(number_of_dots, 10))
    ax.set_title(label_of_image)
    ax.set_xlabel("Время", fontsize=14)
    ax.set_ylabel("Процент онлайна", fontsize=14)
    ax.grid(which="major", linewidth=1.2)
    ax.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)
    ax.scatter(x_axis, y_axis, c="red")
    ax.plot(x_axis, y_axis)
    my_fmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(my_fmt)
    figure.savefig("images/" + label_of_image + ".png")


def create_graph_image(period, total_time, y_axis, label_of_graph):
    number_of_dots = total_time//period
    x = np.linspace(1, number_of_dots, number_of_dots)
    figure, ax = plt.subplots(figsize=(number_of_dots, 10))
    ax.set_title(label_of_graph, fontsize=16)
    ax.set_xlabel("Время", fontsize=14)
    ax.set_ylabel("Процент онлайна", fontsize=14)
    ax.grid(which="major", linewidth=1.2)
    ax.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)
    ax.scatter(x, y_axis, c="red")
    ax.plot(x, y_axis)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    return figure


#figure1 = create_graph_image(1, 11, [1, 2, 3, 4, 5, 64, 40, 8, 7, 5, 9], "28 ноября")
#figure1.savefig("images/plot.png")
create_weekday_image(sample_data, "21")
plt.imsave
create_daily_image(dict_with_data, label_of_image)