# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 18:20:34 2022

@author: nquist

Webscrapper functions
"""
import requests
from bs4 import BeautifulSoup

nums = set([str(i) for i in range(30)])

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

def read_webpage(url, section):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")
    val = soup.find(id=section)
    holder = str(val).replace('<br>', '<br/>')
    content = holder.split('<br/>')
    for i in range(len(content)-1, -1, -1):
        if content[i].strip() == '':
            content.pop(i)
    
    return content

def clean_content(content):
    char_dic = {'“':'"', '”':'"', '’':"'", '—':'--', '…':'...', '‘':"'", '�':'', 'ï':'&#239;', 'é':'&#233;', '–':'-', 'ç':'&#231;', 'ü':'&#252;'}
    chars = ['“', '”', '’', '—', '…', '‘', '�', 'ï', 'é', '–', 'ç', 'ü']
    data_content = 1*content
    types = {'p', 'b', 'strong', 'i', 'em'}
    clean_content = []
    for i in range(len(data_content)):
        line = data_content[i].strip()
        if '>' in line:
            new_line = ''
            temp = line.split('>')
            for part in temp:
                part_clean = part.strip()
                if part_clean != '':
                    start = 0
                    if part_clean[:2] == '</':
                        start = 2
                    elif part_clean[0] == '<':
                        start = 1
                    elif 'google' not in part_clean:
                        new_line += part.strip()
                    if ' ' in part_clean:
                        end = part_clean.index(' ')
                    else:
                        end = len(part_clean)
        
                    if start !=0:
                        tpe = part_clean[start:end]
                        if tpe in types:
                            new_line += part + '>'
            if new_line != '':
                for char in chars:
                    new_line = new_line.replace(char, char_dic[char])
                if new_line != '':
                    clean_content.append(new_line)
        else:
            for char in chars:
                line = line.replace(char, char_dic[char])
            if line != '':
                clean_content.append(line)
        
    
    return clean_content[:-1]

def format_text(content, skip=0, num = False):
    chapters = []
    starts = [0]
    if num:
        for i in range(skip, len(content)-1):
            if content[i].strip() in nums:
                content[i] = 'Chapter ' + content[i]
                starts.append(i)
    else:
        for i in range(skip, len(content)-1):
            if content[i][:7].lower() == 'chapter':
                if content[i][9] not in nums:
                    starts.append(i)
            elif content[i][:7].lower() == 'epilogu':
                starts.append(i)
            elif content[i][:7].lower() == 'prologu':
                starts.append(i)
    
    starts.append(len(content))
    
    skip = False
    for i in range(len(starts)-1):
        line = ''
        for j in range(starts[i+1]-starts[i]):
            if not skip:
                if j == 0 and (content[starts[i]+j].lower()[:7] == 'chapter' or content[starts[i]+j].lower()[:7] == 'epilogu' or content[starts[i]+j].lower()[:7] == 'prologu'):
                    line += '<h2>' + content[starts[i]+j] + '</h2>\n'
                    line += '<p><b>' + content[starts[i]+j+1] + '</b></p>\n\n'
                    skip = True
                else:
                    if starts[i]+j+1 < len(content):
                        nx_line = content[starts[i]+j+1]
                    else:
                        nx_line = 'A'
                    if nx_line[0] != '"' and (nx_line[0].lower() == nx_line[0]):
                        line += '<p>' + content[starts[i]+j] + ' ' + content[starts[i]+j+1] + '</p>\n\n'
                        skip = True
                    else:
                        line += '<p>' + content[starts[i]+j] + '</p>\n\n'
            else:
                skip = False
        chapters.append(line)
    return chapters

def write_xhtml(chapter, title, number):
    f = open('Chapter'+number+'.xhtml', 'w')
    
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n\n')
    f.write('<head>\n\n')
    f.write('<title>' + title +'</title>\n\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write(chapter+'\n')
    f.write('</body>\n')
    f.write('</html>\n')
    
    f.close()
    return True