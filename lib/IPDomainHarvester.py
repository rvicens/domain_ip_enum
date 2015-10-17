#!/usr/bin/env python
# -*- coding: utf8 -*-

from lib.sites.stage1.GoogleSite import *
from lib.sites.stage1.BingSite import *
from lib.sites.stage2.RobtexSite import *
from lib.TargetValidator import *

class IPDomainHarvester():

    def __init__(self):

        self.stage1_sites = { "GOOGLE":GoogleSite(), "BING":BingSite() }
        self.stage2_sites = { "ROBTEX": RobtexSite() }

        self.outfile_base_s1 = "{0}/results/stage1/".format(os.getcwd())
        self.outfile_base_s2 = "{0}/results/stage2/".format(os.getcwd())


        if not os.path.isdir("{0}/results".format(os.getcwd())):
            os.makedirs("{0}/results".format(os.getcwd()))

        if not os.path.isdir("{0}/results/stage1".format(os.getcwd())):
            os.makedirs("{0}/results/stage1".format(os.getcwd()))

        if not os.path.isdir("{0}/results/stage2".format(os.getcwd())):
            os.makedirs("{0}/results/stage2".format(os.getcwd()))


    def store_file(self,fname,content):

        with open(fname,"w+") as f:
            for item in content:
                f.write(item.strip()+"\n")

        return True


    def exec_stage1_sites(self):

        ## exec stage 1 sites
        for site in self.stage1_sites.keys():

            print "*************************************************"
            print "Harvesting domains from: {0}".format(site.upper())
            print "*************************************************"
            s = self.stage1_sites[site]
            s.run()

            urls_file = "{0}{1}_urls.txt".format(self.outfile_base_s1,site.lower())
            print "Storing URLs at: {0}".format(urls_file)
            self.store_file(urls_file,s.urls)

            print "Processing domains..."
            s.get_domains(validate=True)
            domains_file = "{0}{1}_domains.txt".format(self.outfile_base_s1,site.lower())
            print "Storing found domains at: {0}".format(domains_file)
            self.store_file(domains_file,s.domains)

            print "Processing hosts and getting IPs..."
            s.get_ips(validate=True)
            ips_file = "{0}{1}_hosts_ip.txt".format(self.outfile_base_s1,site.lower())
            print "Storing IPs at: {0}\n".format(ips_file)
            self.store_file(ips_file,s.hosts_and_ips)

            networks = []
            tv = TargetValidator(s.keywords,s.urls,s.domains)
            i = IpUtils()
            for item in s.hosts_and_ips:
                ip = item.strip().split(":")[1]

                if not i.checkIfIPinNetworks(ip,networks):
                    w = i.ipWhois(ip)
                    asn_cidr = w["asn_cidr"]
                    for reg_info in w["nets"]:
                        if tv.check_registrant_info(reg_info):
                            if reg_info.has_key("cidr"):
                                tmp = reg_info["cidr"].split(",")
                                if len(tmp) > 1:
                                    networks += tmp
                                else:
                                    asn_cidr = tmp[0]
                                    networks.append(asn_cidr)
                            else:
                                networks.append(asn_cidr)

            networks_file = "{0}{1}_networks.txt".format(self.outfile_base_s1,site.lower())
            print "Storing IPs at: {0}\n".format(networks_file)
            self.store_file(networks_file,networks)

        return True


    def exec_stage2_sites(self):

        ## exec stage 2 sites
        for site in self.stage2_sites.keys():
            print "*************************************************"
            print "Rechecking domains from: {0}".format(site.upper())
            print "*************************************************"
            s = self.stage2_sites[site]
            s.run()

            print "Processing domains..."
            domains_file = "{0}{1}_domains.txt".format(self.outfile_base_s2,site.lower())
            print "Storing found domains at: {0}".format(domains_file)
            self.store_file(domains_file,s.domains)

            print "Processing hosts and getting IPs..."
            ips_file = "{0}{1}_hosts_ip.txt".format(self.outfile_base_s2,site.lower())
            print "Storing IPs at: {0}\n".format(ips_file)
            print s.hosts_and_ips
            self.store_file(ips_file,s.hosts_and_ips)

        return True



    def harvest(self):

        self.exec_stage1_sites()
        self.exec_stage2_sites()

        return True