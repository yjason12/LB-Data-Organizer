import calcmethods
from selenium import webdriver
from urllib.request import urlopen as uReq

import matplotlib.pyplot as plt
import numpy as np


driver = webdriver.Chrome(executable_path="C:/Users/0yong/Downloads/chromedriver_win32/chromedriver.exe")

username =  "yongjaeson"
sortedAvgs = calcmethods.fav_genre(username, driver)

genres = []
avgs = []

for genre in sortedAvgs:
    genres.append(genre)
    avgs.append(round(sortedAvgs[genre], 2))

ypos = np.arange(len(genres))

plt.xticks(ypos, genres)
plt.ylabel("Average Rating")
plt.title("Average Rating By Genre")
plt.bar(ypos, avgs, .8)
plt.ylim([0,10])

for index, value in enumerate(avgs):
    plt.text((index- .3), value, str(value))

plt.xticks(rotation = 45)

plt.show()

driver.close()
