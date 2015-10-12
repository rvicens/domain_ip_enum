#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
from google import search
from lib.TargetValidator import *
from lib.domainUtils import *

class GoogleSite():

    def __init__(self, maxResults="3"):
        self.maxResuts = maxResults
        self.urls = []
        self.domains = []
        self.hosts_and_ips = []
        self.default_keyword_file = "{0}/keywords/google_keywords.txt".format(os.getcwd())
        self.keywords = []


    def get_ips(self, validate=False):

        hosts = []
        u_utils = UrlUtils()
        for url in self.urls:
            host = u_utils.getHost(url)
            ip = u_utils.getIP(url)
            domain = u_utils.getDomain(url)
            if host not in hosts:
                if validate:
                    tv = TargetValidator(self.keywords,self.urls,self.domains)
                    if tv.keywords_at_URL_and_domain(domain,url):
                        hosts.append(host)
                        self.hosts_and_ips.append("{0}:{1}".format(host,ip))
                else:
                    hosts.append(host)
                    self.hosts_and_ips.append("{0}:{1}".format(host,ip))

        return True


    def get_domains(self, validate=False):

        u_utils = UrlUtils()
        for url in self.urls:
            domain = u_utils.getDomain(url)
            if domain not in self.domains:
                if validate:
                    tv = TargetValidator(self.keywords,self.urls,self.domains)
                    if tv.keywords_at_URL_and_domain(domain,url):
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
                print "KEYWORD:{0}".format(keyword)
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
        fp.close()
        '''
        return True