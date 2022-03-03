# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 17:24:52 2022

@author: nquist

Loads website information from ProjectInfo.txt, scrapes the info from the websites
and then formats it into text files and saves it at the file location.
"""
import functions
import os

creation = True
numbering = True

f = open('ProjectInfo.txt', 'r')
lines = f.readlines()
f.close()

folder_name = lines[1].replace(" ", '').strip()
folder_path = lines[11].strip() + '\\' + folder_name
if not os.path.isdir(folder_path):
    os.mkdir(folder_path)
if not os.path.isfile(lines[11].strip() + '\\' + 'ProjectInfo.txt'):
    src ='ProjectInfo.txt'
    dst = lines[11].strip() + '\\' + folder_name + '\\' + 'ProjectInfo.txt'
    os.popen(f"copy {src} {dst}")
os.chdir(folder_path)

if creation:
    urls = functions.make_urls(lines[5][:-1], lines[7][:-1], lines[9][:-1])
    offset = int(lines[13])

    remnent = ''
    ch_count = 1
    for i in range(len(urls)):
        content = functions.read_webpage(urls[i], "textToRead")
        content = functions.clean_content(content)
        if i == 0:
            content = functions.format_text(content, skip = offset, num=numbering)
            file = open('pretext.txt', 'w')
            file.write(content[0])
            file.close()
            content = content[1:]
        else:
            content = functions.format_text(content, num=numbering)
                
        content[0] = remnent + content[0]
        for j in range(len(content)-1):
            chapter = content[j]
            if len(str(ch_count))==1:
                chapter_num = '00' + str(ch_count)
            elif len(str(ch_count))==2:
                chapter_num = '0' + str(ch_count)
            else:
                chapter_num = str(ch_count)
        
            idx = chapter.index('/')
            chapter_title = chapter[4:idx-1]
        
            ret = functions.write_xhtml(chapter, chapter_title, chapter_num)
            ch_count += 1
    
        remnent = content[-1]

    chapter_num = '0' + str(ch_count)
    idx = chapter.index('/')
    chapter_title = chapter[4:idx-1]
    ret = functions.write_xhtml(remnent, chapter_title, chapter_num)

