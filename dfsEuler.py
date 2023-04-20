import requests
from bs4 import BeautifulSoup
import copy

class dfsEuler:
    def __init__(self):
        self.HEAD_URL = "https://www.mathgenealogy.org"
        self.first_soup = BeautifulSoup(requests.get(input("Enter a link ")).content, features='lxml')

    def stepsToEuler(self,soup, steps=0):
        if steps > 20:
            return 0
        links = []
        try:
            for tag in soup.find_all('p'):
                tag_text = tag.getText().strip()
                if "Advisor" in tag_text:
                    a_links = tag.find_all("a")
                    if a_links != None:
                        for a_link in a_links:
                            links.append(a_link["href"])
                            if "Euler" in a_link.getText():
                                return steps + 1
            if len(links) == 0:
                return 0
            else:
                link_steps = []
                #print(links)
                for link in links:
                    next_link = self.HEAD_URL + '/' + link
                    #print(next_link)
                    next_soup = BeautifulSoup(requests.get(next_link).content, features='lxml')
                    link_steps.append(self.stepsToEuler(next_soup, steps + 1))
                #print(link_steps)
                while 0 in link_steps:
                    link_steps.remove(0)
                if len(link_steps) == 0:
                    return 0
                else:
                    return min(link_steps)
        except Exception as e:
            print(e)


    def pathToEuler(self,soup, path=[]):
        if len(path) > 20:
            return None
        links = []
        addedCurrent = False
        EulerFound = False
        try:
            for tag in soup.find_all('p'):
                tag_text = tag.getText().strip()
                if "database" in tag_text:
                    startIndex = tag_text.find("base,") + 6
                    endIndex = tag_text.find("has") -1
                    path.append(tag_text[startIndex:endIndex])
                    addedCurrent = True
                if "Advisor" in tag_text:
                    a_links = tag.find_all("a")
                    if a_links != None:
                        for a_link in a_links:
                            links.append(a_link["href"])
                            if "Euler" in a_link.getText():
                                EulerFound = True

            #IF THERES NO STUDENTS
            if not addedCurrent:
                tag = soup.find("h2", style = "text-align: center; margin-bottom: 0.5ex; margin-top: 1ex")
                tag_text = tag.getText().strip()
                path.append(tag_text)
                addedCurrent = True

            if EulerFound:
                path.append("Euler")
                return path
            if len(links) == 0:
                return None
            else:
                link_steps = []
                for link in links:
                    old_path = copy.deepcopy(path)
                    next_link = self.HEAD_URL + '/' + link
                    next_soup = BeautifulSoup(requests.get(next_link).content, features='lxml')
                    link_steps.append(self.pathToEuler(next_soup, old_path))
                while None in link_steps:
                    link_steps.remove(None)
                if link_steps != []:
                    return min(link_steps, key=len)
                else:
                    return None

        except Exception as e:
            print(e)


    def main(self):
        print(self.stepsToEuler(self.first_soup))
        print(' -> '.join(self.pathToEuler(self.first_soup)))
