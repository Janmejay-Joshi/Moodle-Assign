# Import WebScraping and Form Filling Libraries

from bs4 import BeautifulSoup
import requests
from lxml import html
from csv import reader
from datetime import datetime,timedelta

"""
    Attendance class defing and allocating prerequisits which are required before marking attendance
"""


class Attendance():

    def __init__(self, Session, persist):

        self.session = Session
        self.persist = persist

    def Pretier(self,Details):
        now = datetime.now()
        Pretty = []
        for Detail in Details:
            Time_Left = str(datetime.strptime(Detail[1],"%A, %d %B %Y, %I:%M %p") - now)[:-7]
            if (Time_Left[0] != "-"):
                Detail.append(Time_Left)
                Pretty.append(Detail)
        return Pretty;

    def Find_Link(self, Lecture):

        result = self.session.get(Lecture, headers = dict(referer = Lecture))
        soup = BeautifulSoup(result.content, 'lxml')
        Sections = soup.findAll("li",attrs={"class":"section main clearfix"})

        for Section in Sections:
            try:
                Title = Section.find("h3",attrs={"class":"sectionname"}).find('a').contents 
                Quizes = Section.find_all("li", attrs={"class":"activity quiz modtype_quiz"})
                Quizes_Links = [ Quiz.find("a",attrs={"class":"aalink"})['href'] for Quiz in Quizes]

                Assingments = Section.find_all("li", attrs={"class":"activity assign modtype_assign"})
                Assingments_Links = [ Assingment.find("a",attrs={"class":"aalink"})['href'] for Assingment in Assingments]


                Details = [self.Find_Due(Lecture,Assingments_Link) for Assingments_Link in Assingments_Links]
                if Details != []:
                    print(Title)
                    return self.Pretier(Details)[0]

            except Exception:
                pass


    def Find_Due(self,Lecture, Link):

        result = self.session.get(Link , headers = dict(referer = Lecture))
        soup = BeautifulSoup(result.content, 'lxml')

        Table = soup.find("table",attrs={"class":"generaltable"})
        Main = soup.find("div", attrs={"role":"main"})

        Title = Main.find("h2").contents[0]

        try:
            Table.find("td", attrs={"class":"submissionstatussubmitted cell c1 lastcol"}).contents[0]
            Due = Table.find("td",attrs={"class":"cell c1 lastcol"}).contents[0]
            Status = "Done";

        except Exception:
            Due = Table.find_all("td",attrs={"class":"cell c1 lastcol"})[1].contents[0]
            Status = "Due";

        return [Title,Due,Status]


