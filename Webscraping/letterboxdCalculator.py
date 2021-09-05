from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver

username = 'yongjaeson' #input("Enter Letterboxd Account Username: ")

filmsHomePage = 'https://letterboxd.com/' + username + '/films/'

#set up browser
driver = webdriver.Chrome(executable_path='C:/Users/0yong/Downloads/chromedriver_win32/chromedriver.exe')
driver.get(filmsHomePage)
page = driver.page_source
page_soup = soup(page, 'html.parser')


#break down html to get pages
listOfPageCount = page_soup.findAll("li",{"class":"paginate-page"})
lineWithPageCount = listOfPageCount[len(listOfPageCount) -1]
lastPage = lineWithPageCount.a

numPages = 0;
i = 0
test = str(lastPage)
while (test[22 + len(username) + i] != '/'):
    numPages = numPages * 10
    numPages = numPages + int(test[22 + len(username) + i])
    i+=1


#Loop through each page and determine average
numMovies = 0
totalRating = 0
pageLink = filmsHomePage + 'page/'


for i in range(1, numPages + 1, 1):
    newLink = pageLink + str(i)
    driver.get(newLink)


    page = driver.page_source
    page_soup = soup(page, 'html.parser')

    containers = page_soup.findAll("p",{"class":"poster-viewingdata -rated-and-liked"})
    for container in containers:
        ratingTag = container.span

        if ratingTag is None:
            continue
        elif ((str(ratingTag))[13] == 'l'):
            continue

        if((str(ratingTag))[41] == '0'):
            numMovies+=1
            totalRating+=10
            continue

        totalRating+=int((str(ratingTag))[40])

        numMovies+=1

driver.close()
print(totalRating)
print(numMovies)
print('average: ' + str(totalRating/numMovies))
