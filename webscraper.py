# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 17:24:52 2022

@author: nquist

Loads website information from ProjectInfo.txt, scrapes the info from the websites
and then formats it into text files and saves it at the file location.
"""
import functions

import requests
import urllib.request

f = open('ProjectInfo.txt', 'r')
lines = f.readlines()
urls = functions.make_urls(lines[5][:-1], lines[7][:-1], lines[9][:-1])