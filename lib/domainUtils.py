#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import urlparse
import whois
import re

from ipwhois import IPWhois
from tld import get_tld
from tld.utils import update_tld_names


class IpUtils():
    def __init__(self, update_TLD=False):
        pass

    def checkIfIP(self, ip):
        out = False
        try:
            socket.inet_aton(ip)
            out = True
        except socket.error:
            out = False
        return out

    def ipWhois(self, ip):
        out = None
        try:
            if self.checkIfIP(ip):
                obj = IPWhois(ip)
                out = obj.lookup()
        except:
            out = None
            pass

        return out


class DomainUtils():
    def __init__(self, update_TLD=False):
        pass

    def getWhois(self, domain):
        # >>> print(domain.__dict__)
        # {'expiration_date': datetime.datetime(), 'last_updated': datetime.datetime(), 'registrar': 'aaa', 'name': 'bb', 'creation_date': datetime.datetime()}
        # >>> print(domain.name)
        # google.com

        try:
            whois_result = whois.query(str(domain))
        except:
            whois_result = None
            pass

        return whois_result


class UrlUtils():
    def __init__(self, url=None, update_TLD=False):
        # self.url = url
        if update_TLD:
            update_tld_names()

    def isUrl(self, url):

        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if url.startswith("www."): url = "http://" + url
        return re.match(regex, str(url))

    def getDomain(self, url):
        try:
            if self.isUrl(url):
                return get_tld(url)
            else:
                return None
        except:
            pass
            return None

    def getHost(self, url):
        if self.isUrl(url):
            return urlparse.urlparse(url).hostname
        else:
            return None

    def getIP(self, url):
        host = self.getHost(url)
        try:
            addr = socket.gethostbyname(host)
        except:
            addr = None
            pass

        return addr

    def getPath(self, url):
        if "." in self.getEndResource(url):
            out = os.path.dirname(urlparse.urlparse(url).path)
        else:
            out = urlparse.urlparse(url).path
        return out

    def getEndResource(self, url):
        out = os.path.basename(urlparse.urlparse(url).path)
        if "." in out:
            return "/" + out
        else:
            out = ""
            return out

    def getProto(self, url):
        up = urlparse.urlparse(url)
        out = up.scheme
        return out

    def getPort(self, url):
        up = urlparse.urlparse(url)
        out = up.port
        if out:
            return out
        else:
            proto = up.scheme
            if proto == "https":
                out = "443"
            else:
                out = "80"
            return out
