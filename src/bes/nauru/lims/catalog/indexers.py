# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

from bika.lims.interfaces.analysis import IRequestAnalysis
from plone.indexer import indexer


@indexer(IRequestAnalysis)
def date_sampled(instance):
    """Returns the date when the sample the analysis belongs to was collected
    """
    sample = instance.getRequest()
    return sample.getDateSampled()
