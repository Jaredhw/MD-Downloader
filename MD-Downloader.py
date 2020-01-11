# Tested using Win 10 Pro - 1809 & Python 3.8.1 32-bit 
# It"s highly suggested you use a Python3 >= Version 3.4 so PIP is bundled. 

#Enables debug output
DEBUG = False
mangaList = []
print("MangaDex Webscraping tool by @SeveralDogs")
# Attempts to import or install then import dependencies
import subprocess
import sys
import json
import os

# Attempts to install dependencies using pip through Windows commandline calls
# It may require seting Python up in windows PATH
try:
    from bs4 import BeautifulSoup 
except ModuleNotFoundError:  #Install BS4 if it"s not installed.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"]) 
    from bs4 import beautifulsoup4
try:
    import lxml
except ModuleNotFoundError:  #Installs lxml if not already installed
    subprocess.check_call([sys.executable, "-m", "pip", "install", "lxml"]) 
    import lxml

#Prints information about the current dependencies to the console
if DEBUG == True:
    print("---- LXML INFORMATION ----")
    subprocess.check_call([sys.executable, "-m", "pip", "show", "lxml"]) 
    print("---- BS4 INFORMATION ----")
    subprocess.check_call([sys.executable, "-m", "pip", "show", "beautifulsoup4"]) 

class Manga:
    def __init__(self, title, originalLanguage, author, status, userScore, bayScore):
        self.title = title
        self.originalLanguage = originalLanguage
        self.author = author
        self.status = status
        self.userScore = userScore
        self.bayScore = bayScore

# Checks the current directory for files and stores all ".html" files into a list
print("Checking .py file directory for .HTML files, NOTE: Does not search subdirectories")

htmlFiles = []
files = [f for f in os.listdir(".") if os.path.isfile(f)]
for f in files:
    # only move the file forward if it ends with .html
    if f.lower().endswith((".html")) == True:
        htmlFiles.append(f)

# Prints information about files found to the console
print("HTML Files Detected: ")
for htmlFile in htmlFiles:
  print(htmlFile)       

# Iterates through a list of HTML files and searches each one for a set of pre-defined tags.
with open("test.html", encoding="utf-8") as rawHTML:
    soup = BeautifulSoup(rawHTML, "lxml")
    currentPage = soup.find_all(class_="manga-entry")
    for manga in currentPage:
        section1 = manga.find(class_="col-lg-7")
        # Searches for a tag with a specific tag and then looks for and extracts the value of the title for that tag
        title = section1.find(class_="manga_title")["title"]
        print("Title: " + title )

        #TODO - The website has the tag of Chinese(Trad) but the flag is the Hong Kong flag while China uses Chinese(Simp) and uses the Chinese Flag, determine which is correct
        origLanguage = manga.find(class_="flag")["title"]
        print("Original Language: " + origLanguage)

        # Searches for a tag with a specific tag then navigates down two levels, in this specific case from "div" to "a" to "title" Requires that "a" is the first child of the "col-3" div tag
        #TODO - Better implimentation that doesn"t rely on the tags to be in a specific order
        author = manga.find(class_="col-3").contents[0]["title"]
        print("Author(s): " + author)

        # Searches for the span that contains the current reading status and pulls the text out from between the span tags
        status = manga.find(class_="d-xl-inline").getText()
        print("Current Status: " + status)

        #
        section2 = manga.find(class_="col-lg-5")
        userScore = section2.find(class_="dropdown-toggle").getText()
        print("User Score:" + userScore , end="")

        data = section2.find_all(class_="p-1 col text-center text-primary")
        bayScore = data[1].getText()
        print("Bayesian Score: " + data[1].getText())
        print("------------------------------------------------")
       

        





# Writes the data scrapped from the HTML files into a json file
# with open("data.txt", "w", encoding="utf-8") as f:
    # json.dump(data, f, ensure_ascii=False)
    # Name, Author, User Status, User Rating, Bayesian Rating, Original Language