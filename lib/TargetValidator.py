#!/usr/bin/env python
# -*- coding: utf8 -*-

from lib.domainUtils import *

class TargetValidator():

    def __init__(self,keywords,urls,domains):
        self.urls = urls
        self.domains = domains
        self.keywords = keywords


    def keywords_at_URL_and_domain(self,domain,url):

        for key in self.keywords:
            if key in domain:
                return True

        u_utils = UrlUtils()

        for key in self.keywords:
            path = u_utils.getPath(url)
            if key in path and key not in domain:
                return False

        return False


    def check_registrant_info(self,reg_info):

        name = reg_info["name"] if reg_info.has_key("name") else ""
        desc = reg_info["description"] if reg_info.has_key("description") else ""
        tech_emails = reg_info["tech_emails"] if reg_info.has_key("tech_emails") else ""
        abuse_emails = reg_info["abuse_emails"] if reg_info.has_key("abuse_emails") else ""

        if name and desc:
            for keyw in self.keywords:
                if keyw in name or keyw in desc:
                    return True

        if tech_emails and abuse_emails:
            for dom in self.domains:
                if dom in tech_emails or dom in abuse_emails:
                    return True

        return False