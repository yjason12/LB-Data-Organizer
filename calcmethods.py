# calcmethods.py
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver

def fav_genre(username):
    page ="https://letterboxd.com/" + username + "/films"

    genres = ["war", "adventure", "animation", "comedy", "crime",
            "documentary", "drama", "family", "fantasy", "history",
            "horror", "music", "mystery", "romance", "science-fiction",
            "thriller", "tv-movie", "war", "western"]

    genreAvgs = {}

    for genre in genres:
        genreAvgs[genre] = genre_avg(genre,username)

    sortedAvgs = sorted(genreAvgs.items(), key = lambda kv: kv[1])
    sortedAvgs = dict(sortedAvgs).reverse()
    for genre in sortedAvgs:
        print("average rating for " + genre + ": " + str(sortedAvgs[genre]))



def genre_avg(genre, username):

    genrePage ="https://letterboxd.com/" + username + "/films/genre/" + genre +"/"

    #set up browser and open page
    driver = webdriver.Chrome(executable_path="C:/Users/0yong/Downloads/chromedriver_win32/chromedriver.exe")
    driver.get(genrePage)
    page = driver.page_source
    page_soup = soup(page, "html.parser")


    #determine page count
    listOfPageCount = page_soup.findAll("li", {"class":"paginate-page"})
    if(len(listOfPageCount) == 0):
        lastPage = 1
    else:
        lineWithPageCount = listOfPageCount[len(listOfPageCount) -1]
        lastPage = lineWithPageCount.a
        splitList = str(lastPage).split("/")
        lastPage = splitList[len(splitList) - 3]


    #Loop through each page and determine average
    numMovies = 0
    totalRating = 0
    pageLink = genrePage + "page/"
    for i in range(1, int(lastPage) + 1, 1):
        newLink = pageLink + str(i)
        driver.get(newLink)

        page = driver.page_source
        page_soup = soup(page, "html.parser")

        containers = page_soup.findAll("p",{"class":"poster-viewingdata -rated-and-liked"})
        for container in containers:
            ratingTag = container.span

            if ratingTag is None: #no rating
                continue

            tagArr = str(ratingTag).split("\"")

            if(len(tagArr) != 3): #no rating
                continue

            tagArr = tagArr[1] #get rating from tag
            tagArr = tagArr.split("-")
            numMovies+=1
            totalRating+=int(tagArr[3])

    driver.close()
    #print("total Rating " + str(totalRating))
    #print("numMovies " + str(numMovies))
    if(numMovies == 0):
        return 0
    return totalRating/numMovies
