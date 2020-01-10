# Tested using Win 10 Pro - 1809 & Python 3.8.1 32-bit 

#Enables debug output
DEBUG = False


print("MangaDex Webscraping tool by @SeveralDogs")

# Attempts to import or install then import dependencies
import subprocess
import sys
import json
import os

try:
    from bs4 import BeautifulSoup 
except ModuleNotFoundError:  #Install pip if it's not installed. May require adding python to PATH on Windows.    
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4']) 
    from bs4 import beautifulsoup4
try:
    import lxml
except ModuleNotFoundError:    
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lxml']) 
    import lxml

if DEBUG == True:
    print("---- LXML INFORMATION ----")
    subprocess.check_call([sys.executable, '-m', 'pip', 'show', 'lxml']) 
    print("---- BS4 INFORMATION ----")
    subprocess.check_call([sys.executable, '-m', 'pip', 'show', 'beautifulsoup4']) 


# Checks the current directory for files and stores all ".html" files into a list
print("HTML Files Detected: ")
htmlFiles = []
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    # only move the file forward if it ends with .html
    if f.lower().endswith(('.html')) == True:
        htmlFiles.append(f)
for htmlFile in htmlFiles:
  print(htmlFile)       

# Iterates through a list of HTML files and searches each one for a set of pre-defined tags.
with open("test.html", encoding="utf-8") as rawHTML:
    soup = BeautifulSoup(rawHTML, "lxml")
    
    # Searches the HTML Soup and put each instance of the column class contents into an interable variable
    for manga in soup.find_all(class_="col-md-6 col-lg-7"):
        # Searches for a tag with a specific tag and then looks for and extracts the value of the title for that tag
        print("Title: " + manga.find(class_="manga_title")['title'])
        
        #TODO - The website has the tag of Chinese(Trad) but the flag is the Hong Kong flag while China uses Chinese(Simp) and uses the Chinese Flag, determine which is correct
        print("Original Language: " + manga.find(class_="flag")['title'])

        # Searches for a tag with a specific tag then navigates down two levels, in this specific case from "div" to "a" to "title" Requires that "a" is the first child of the "col-3" div tag
        #TODO - Better implimentation that doesn't rely on the tags to be in specific
        print("Author(s): " + manga.find(class_="col-3").contents[0]['title'])
        print("------------------------------------------------")

        
       

        





# Writes the data scrapped from the HTML files into a json file
# with open('data.txt', 'w', encoding="utf-8") as f:
    # json.dump(data, f, ensure_ascii=False)
    # Name, Author, User Status, User Rating, Bayesian Rating, Original Language