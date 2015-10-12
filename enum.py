#!/usr/bin/env python
# -*- coding: utf8 -*-

from lib.IPDomainHarvester import *

if __name__ == '__main__':

    domains = IPDomainHarvester()
    domains.harvest()