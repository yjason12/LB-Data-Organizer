# calcmethods.py
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver

def calc_genre_avg(genre, username):

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
            elif ((str(ratingTag))[13] == "l"): #no rating
                continue

            if((str(ratingTag))[41] == "0"): #rating is a 10
                numMovies+=1
                totalRating+=10
                continue

            totalRating+=int((str(ratingTag))[40])
            numMovies+=1

    driver.close()
    print("total Rating " + str(totalRating))
    print("numMovies " + str(numMovies))
    return totalRating/numMovies
