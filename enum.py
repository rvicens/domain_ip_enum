#!/usr/bin/env python
# -*- coding: utf8 -*-

from lib.DomainHarvester import *


if __name__ == '__main__':

    domains = DomainHarvester()
    domains.harvest(["google"])