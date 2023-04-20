import requests
from bs4 import BeautifulSoup
import copy

class bfsEuler:
    def __init__(self):
        self.HEAD_URL = "https://www.mathgenealogy.org"
        self.first_soup = BeautifulSoup(requests.get(input("Enter a link ")).content, features='lxml')

    def stepsToEuler(self,soup):
        steps = []
        queue = [(soup,0)]
        while len(queue) > 0:
            thisSoup, thisStep = queue.pop(0)
            if thisStep < 10:
                links = []
                for tag in thisSoup.find_all('p'):
                    tag_text = tag.getText().strip()
                    if "Advisor" in tag_text:
                        a_links = tag.find_all("a")
                        if a_links != None:
                            for a_link in a_links:
                                #Add all possible parents to list
                                links.append(a_link["href"])
                                #If Euler is a possible parent, add this path's step count to the steps list
                                if "Euler" in a_link.getText():
                                    steps.append(thisStep+1)
                if len(links) > 0:
                    for link in links:
                        #Add all possible links to queue
                        next_link = self.HEAD_URL + '/' + link
                        next_soup = BeautifulSoup(requests.get(next_link).content, features='lxml')
                        queue.append((next_soup,thisStep+1))
        #Return the shortest steps taken to reach Euler
        return min(steps)

    def pathToEuler(self,soup):
        paths = []
        queue = [(soup, [])]
        while len(queue) > 0:
            thisSoup, thisPath = queue.pop(0)
            if len(thisPath) < 10:
                links = []
                addedCurrent = False
                EulerFound = False
                for tag in thisSoup.find_all('p'):
                    tag_text = tag.getText().strip()
                    if "database" in tag_text:
                        startIndex = tag_text.find("base,") + 6
                        endIndex = tag_text.find("has") - 1
                        thisPath.append(tag_text[startIndex:endIndex])
                        addedCurrent = True
                    if "Advisor" in tag_text:
                        a_links = tag.find_all("a")
                        if a_links != None:
                            for a_link in a_links:
                                links.append(a_link["href"])
                                if "Euler" in a_link.getText():
                                    EulerFound = True

                # IF THERES NO STUDENTS
                if not addedCurrent:
                    tag = soup.find("h2", style="text-align: center; margin-bottom: 0.5ex; margin-top: 1ex")
                    tag_text = tag.getText().strip()
                    thisPath.append(tag_text)
                    addedCurrent = True

                if EulerFound:
                    thisPath.append("Euler")
                    paths.append(thisPath)

                if len(links) > 0:
                    for link in links:
                        old_path = copy.deepcopy(thisPath)
                        next_link = self.HEAD_URL + '/' + link
                        next_soup = BeautifulSoup(requests.get(next_link).content, features='lxml')
                        queue.append((next_soup,old_path))

        return min(paths, key=len)



    def main(self):
        print(self.stepsToEuler(self.first_soup))
        print(' -> '.join(self.pathToEuler(self.first_soup)))

