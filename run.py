import calcmethods

username =  "yongjaeson"
genre = "horror"
dramaAvg = calcmethods.calc_genre_avg(genre, username)

print(username + "\'s average rating for " + genre + " is " + str(dramaAvg))
