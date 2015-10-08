#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
from google import search
from lib.domainUtils import *

class GoogleSite():

    def __init__(self, maxResults="5"):
        self.maxResuts = maxResults
        self.urls = []
        self.domains = []
        self.default_keyword_file = "{0}/keywords/google_keywords.txt".format(os.getcwd())
        self.keywords = []

    def validate(self,domain,url):

        for key in self.keywords:
            if key in domain:
                return True

        u_utils = UrlUtils()

        for key in self.keywords:
            path = u_utils.getPath(url)
            if key in path and key not in domain:
                return False

        return False

    def get_domains(self, validate=False):

        u_utils = UrlUtils()
        for url in self.urls:
            domain = u_utils.getDomain(url)
            if domain not in self.domains:
                if validate:
                    if self.validate(domain,url):
                        self.domains.append(domain)
                else:
                    self.domains.append(domain)

        return True


    def run(self, keywords=[]):

        if not keywords:
            # Check if file exists
            if not os.path.isfile(self.default_keyword_file):
                return False
            else:
                keywords = []
                fp = open(self.default_keyword_file,"r")
                for line in fp.readlines():
                    keywords.append(line.strip())
                fp.close()

        self.keywords = keywords
        print "Using Keywords:{0}".format(self.keywords)

        try:
            # Get the hits for the given keywords
            for keyword in self.keywords:
                for url in search(keyword, stop=self.maxResuts):
                    print "Found URL:{0}".format(url)
                    self.urls.append(url)
        except:
                print "Something went wrong scraping Google."
                print "Scraping has stopped"
                pass

        ### TEMPORAL ###
        '''
        fp = open("test_urls","r")
        urls = fp.readlines()
        for u in urls:
            u = u.strip()
            self.urls.append(u)
        '''

        return True