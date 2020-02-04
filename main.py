#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List
from pandas import DataFrame

def get_mails(path: str, limit: int = None) -> List[str]:
    '''Extract emails from an .mbox file.'''
    mails = []
    c = -1
    mail = str()
    with open(path, 'r', encoding = 'UTF-8') as file:
        for line in file:               #read every line
            if c == limit: break
            if line.startswith('From'): #when a new mail starts...
                c += 1                  #add it to the counter
                print(c)
                mails.append(mail)      #add the lines that you've been saving
                mail = line             #reset the mail text to the first line
            else:
                mail += line            #add each line to the mail text
    return mails[1:]                    #first line is redudant

def add_unsubscribe(mails: List, unsub_links: dict = {}) -> dict:
    for mail in mails:
        #getting sender
        sender_line = mail.split('\n')[0]               #first line of the mail
        sender_words = sender_line.split(' ')[1:]       #removes the 'From: ' part
        sender = ' '.join(sender_words)                 #recreates the name string
        if 'Q?' in sender:
            sender = re.findall('.Q.?(.*?)\?', sender)[0]  #removing some char coding
        #getting unsubscribe links
        for line in mail.split('\n'):
            if 'List-Unsubscribe' in line and '<' in line:
                links = re.findall('<(.*?)>', line)
                url = mailto = None
                for link in links:
                    if link.startswith('https'):
                        url = link
                    elif link.startswith('mailto'):
                        mailto = link
                if any(links):
                    if sender in unsub_links:
                        unsub_links[sender]['count'] += 1
                    else:
                        unsub_links[sender] = {'count': 1, 'url': url, 
                                               'mailto': mailto}
    return unsub_links

def main():
    path = 'input/mail.mbox'
    mails = get_mails(path)
    unsub_links = add_unsubscribe(mails)
    df = DataFrame(unsub_links).T
    df = df.sort_values(by='count', ascending=False)
    df.to_csv('output.csv')
    
if __name__ == "__main__":
    main()