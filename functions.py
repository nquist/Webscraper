# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 18:20:34 2022

@author: nquist

Webscrapper functions
"""

def make_urls(starting_url, ending_url, page_num, btype=1):
    url_list = []
    if btype == 1:
        url_list.append(starting_url+ending_url)
    else:
        temp_url = starting_url + 'page,1,' + ending_url
        url_list.append(temp_url)
    
    if int(page_num) > 1:
        for i in range(2, int(page_num)+1):
            temp_url = starting_url + 'page,'+str(i)+',' + ending_url
            url_list.append(temp_url)
    
    return url_list