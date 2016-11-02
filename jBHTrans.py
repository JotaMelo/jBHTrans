#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


class jBHTrans:
    locationMainPage = u"http://servicosbhtrans.pbh.gov.br/bhtrans/bhtmobile/app_sinotico.asp"
    locationLinePage = u"http://servicosbhtrans.pbh.gov.br/bhtrans/bhtmobile/app_sinotico2a.asp?linha={0}&nome={1}"

    def getSoup(self, url, **kwargs):
        req = requests.get(url, **kwargs)
        return BeautifulSoup(req.text)

    def parseLocationHTML(self, html):
        response = {}

        lines = html.split("<br />")
        response["time"] = lines[0].split("Horario: ")[1].strip()
        response["address"] = lines[1].strip()
        response["direction"] = lines[2].split("Sentido:")[1][:-1].strip().title()

        return response

    def getAvailableBusLines(self):
        soup = self.getSoup(self.locationMainPage)
        response = []
        for i in soup.find_all(attrs={"data-theme": "c"}):
            linkQuery = i.find("a")["href"].split("?")[1]
            lineInfo = {
                "lineNumber": linkQuery.split("linha=")[1].split("&")[0],
                "lineName": linkQuery.split("nome=")[1].title()
            }
            response.append(lineInfo)

        return response

    def getBusLocations(self, lineNumber, lineName):
        url = self.locationLinePage.format(lineNumber, lineName)
        soup = self.getSoup(url)

        mainScriptNode = soup.find("script", attrs={"src": None})
        lines = mainScriptNode.text.split("\n")

        relevantVariables = ["pontosLt", "pontosLg", "html"]

        response = []
        for line in lines:
            line = line.strip()
            variableName = line.split("[")[0]

            if variableName in relevantVariables:
                index = int(line.split("[")[1].split("]")[0])
                value = line.split("=")[1][:-1].strip()

                if index >= len(response):
                    response.append({})

                if variableName == "pontosLt":
                    response[index]["latitude"] = float(value)
                elif variableName == "pontosLg":
                    response[index]["longitude"] = float(value)
                elif variableName == "html":
                    htmlData = self.parseLocationHTML(value)
                    response[index].update(htmlData)

        return response
