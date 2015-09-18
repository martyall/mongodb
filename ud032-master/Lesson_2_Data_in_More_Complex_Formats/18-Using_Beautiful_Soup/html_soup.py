#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI
# All your changes should be in the 'extract_data' function

from bs4 import BeautifulSoup
import requests
import json

html_page = "page_source.html"


def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    soup = BeautifulSoup(open(html_page), "xml")
    events = soup.find_all(id="__EVENTVALIDATION")
    for event in events:
        print event
        data["eventvalidation"] = event["value"]
    states = soup.find_all(id="__VIEWSTATE")
    for state in states:
        print state
        data["viewstate"] = state["value"]
    return data


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    data = extract_data(html_page)
    print data["eventvalidation"] != ""
    #print data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
    assert data["viewstate"].startswith("/wEPDwUKLTI")
    
    
test()
