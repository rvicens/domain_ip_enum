#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import requests
from bs4 import BeautifulSoup
from lib.domainUtils import *

class RobtexSite():

    def __init__(self):

        self.domains = []
        self.hosts_and_ips = []
        self.base_url  = "https://www.robtex.com/route/"
        self.page = ""

        self.check_networks = []
        self.input_files_dir = "{0}/results/stage1/".format(os.getcwd())
        if os.path.isdir(self.input_files_dir):
            for f in os.listdir(self.input_files_dir):
                if "networks" in f:
                    fp = open("{0}{1}".format(self.input_files_dir,f),"r")
                    lines = fp.readlines()
                    for line in lines:
                        line = line.strip()
                        if line not in self.check_networks:
                            self.check_networks.append(line)


    def pase_page(self):

        soup = BeautifulSoup(self.page,"html5lib")

        tblIP = soup.find_all('table', {'class': 'sortable noinit scrollable noanchor'})
        if len(tblIP) > 0:
            th = tblIP[0].find('th', text='Hostname')
            if th:
                rows = tblIP[0].find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) > 0:
                        ## GET HOST:IP info
                        ip = cells[0].get_text().encode("utf-8").strip()
                        host = cells[2].get_text().encode("utf-8").strip().lower()
                        if "{0}:{1}".format(host,ip) not in self.hosts_and_ips:
                            self.hosts_and_ips.append("{0}:{1}".format(host,ip))

                        ## GET DOMAINS
                        u = "http://{0}".format(host)
                        u_utils = UrlUtils()
                        dom = u_utils.getDomain(u)
                        if dom not in self.domains and dom != None:
                            self.domains.append(dom)

        return True


    def get_page(self,url):

        try:
            r = requests.get(url, verify=False, timeout=60 )
            self.page = r.text
        except Exception, e:
            print "Something went wrong querying Robtex at URL:{0}".format(url)
            return False

        return True


    def run(self):

        for net in self.check_networks:
            net = net.strip()
            ip_net = net.replace("/","-")
            url = "{0}{1}.html".format(self.base_url,ip_net)
            self.get_page(url)
            self.pase_page()

        return True
