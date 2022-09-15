# calcmethods.py
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver

# Given a user and a webdriver, return a sorted list of genres by average rating
def fav_genre(username, driver):
    page ="https://letterboxd.com/" + username + "/films"

    genres = ["action", "adventure", "animation", "comedy", "crime",
            "documentary", "drama", "family", "fantasy", "history",
            "horror", "music", "mystery", "romance", "science-fiction",
            "thriller", "tv-movie", "war", "western"]

    genreAvgs = {}

    for genre in genres:
        genreAvgs[genre] = genre_avg(genre, username, driver)

    sortedAvgs = sorted(genreAvgs.items(), key = lambda kv: kv[1])
    sortedAvgs = dict(sortedAvgs)
    for genre in sortedAvgs:
        print("average rating for " + genre + ": " + str(sortedAvgs[genre]))

    return sortedAvgs


# Given a genre and user, parse through user data and return the user's average rating for the genre
def genre_avg(genre, username, driver):

    genrePage ="https://letterboxd.com/" + username + "/films/genre/" + genre +"/"

    # set up browser and open page
    driver.get(genrePage)
    page = driver.page_source
    page_soup = soup(page, "html.parser")


    # determine page count
    listOfPageCount = page_soup.findAll("li", {"class":"paginate-page"})
    if(len(listOfPageCount) == 0):
        lastPage = 1
    else:
        lineWithPageCount = listOfPageCount[len(listOfPageCount) -1]
        lastPage = lineWithPageCount.a
        splitList = str(lastPage).split("/")
        lastPage = splitList[len(splitList) - 3]


    # Loop through each page and determine average
    numMovies = 0
    totalRating = 0
    pageLink = genrePage + "page/"
    for i in range(1, int(lastPage) + 1, 1):
        newLink = pageLink + str(i)
        driver.get(newLink)

        page = driver.page_source
        page_soup = soup(page, "html.parser")

        containers = page_soup.findAll("p",{"class":"poster-viewingdata -rated-and-liked"})
        # Iterate through every movie entry in page
        for container in containers:
            
            # Retrieve rating from movie entry
            ratingTag = container.span

            if ratingTag is None: # no rating
                continue

            tagArr = str(ratingTag).split("\"")

            if(len(tagArr) != 3): #no rating
                continue

            tagArr = tagArr[1] #get rating from tag
            tagArr = tagArr.split("-")
            numMovies+=1
            totalRating+=int(tagArr[3])

    #print("total Rating " + str(totalRating))
    #print("numMovies " + str(numMovies))
    if(numMovies == 0):
        return 0
    return totalRating/numMovies
