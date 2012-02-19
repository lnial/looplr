#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib
import feedparser
from BeautifulSoup import BeautifulSoup
import sched, time
import random
import shutil


s = sched.scheduler(time.time, time.sleep)
URL_LIST   = []
HASH_TABLE = []
HAVE_JPG = 10000

def make_url_list():
    atomfeed = "http://mao.s151.xrea.com/tumbrowser/new.xml"
    atom = feedparser.parse(atomfeed)
    """
    make_url_list
    >>> make_url_list()
    '1'
    # e.g.)
    URL_LIST = (
        #"http://30.media.tumblr.com/tumblr_lr8sl08r0p1qzcd3bo1_500.jpg", 
        #"http://30.media.tumblr.com/tumblr_lr8sl08r0p1qzcd3bo1_500.jpg", 
    #)
    """
    for channel in atom['entries']:
        data = channel['summary_detail']['value']
        soup = BeautifulSoup(data)
        elements = soup.findAll('img')
        for e in elements:
            URL_LIST.append(e['src'])
            #print e['src']
            #http://30.media.tumblr.com/tumblr_lr8sl08r0p1qzcd3bo1_500.jpg

def download(url):
	img = urllib.urlopen(url)
	localfile = open( "./photos/%s" % os.path.basename(url), 'wb')
	localfile.write(img.read())
	img.close()
	localfile.close()

def get_photo():
    """downloard photo"""
    make_url_list()
    for url in URL_LIST:
        if len(HASH_TABLE) >= HAVE_JPG and not url in HASH_TABLE:
            download(url)
            #for next time delete
            #HAVE_JPG only number
            os.remove(os.getcwd() + "/photos/" + os.path.basename(HASH_TABLE[0]))
            print "delete" + HASH_TABLE[0]
            del HASH_TABLE[0]
            HASH_TABLE.append(url)

        elif len(HASH_TABLE) < HAVE_JPG and not url in HASH_TABLE:
            download(url)
            HASH_TABLE.append(url)
    del URL_LIST[:]

def random_copy():
    """jpg from photos folder to shows folfer"""
    file_list=os.listdir(os.getcwd() + "/photos/")
    for i in range(0, 21):
        index = random.randrange(0, len(file_list), 2)
        i_file_name = file_list[index]
        shutil.copyfile(os.getcwd() + "/photos/" + i_file_name, os.getcwd() + "/shows/" + str(i) + ".jpg")



if __name__ == '__main__':
    #sched loop
    while True:
        s.enter(1800, 1, get_photo, ()) 
        for i in range(0, 180):
            s.enter(i * 10, 1, random_copy, ()) 
        s.run()

