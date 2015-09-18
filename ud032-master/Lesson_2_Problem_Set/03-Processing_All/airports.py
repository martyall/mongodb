#!/usr/bin/env python
# -*- coding: utf-8 -*-
# All your changes should be in the 'extract_airports' function
# It should return a list of airport codes, excluding any combinations like "All"

from bs4 import BeautifulSoup
import re
html_page = "options.html"


def extract_airports(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, 'html.parser')
        airport_list_element = soup.find(id="AirportList")
        airports = airport_list_element.find_all(name="option")
        all_re = re.compile(r"All")
        for airport in airports:
            if not all_re.match(airport["value"]):
                data.append(airport["value"])
    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()
