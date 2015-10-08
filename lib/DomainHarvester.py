#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
from lib.GoogleSite import *

class SiteLauncher():

    def __init__(self):
        self.sites = {"GOOGLE":GoogleSite()}

    def get(self,site):
        return self.sites[site]


class DomainHarvester():

    def __init__(self):

        self.high_confidence = []
        self.low_confidence = []
        self.outfile_base = "{0}/results/harvest_google".format(os.getcwd())

    def harvest(self,sites):

        sl = SiteLauncher()
        for site in sites:
            if site.upper() in sl.sites.keys():
                print "*************************************************"
                print "Harvesting domains from: {0}".format(site.upper())
                print "*************************************************"
                s = sl.get(site.upper())
                s.run()
                s.get_domains(validate=True)
                with open("{0}_domains.txt".format(self.outfile_base),"w+") as f:
                    for d in s.domains:
                        f.write(d+"\n")
                with open("{0}_urls.txt".format(self.outfile_base),"w+") as f:
                    for u in s.urls:
                        f.write(u+"\n")
        return True