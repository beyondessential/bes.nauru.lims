# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

from bes.lims.interfaces import IBESLimsLayer


class IBesNauruLimsLayer(IBESLimsLayer):
    """Zope 3 browser Layer interface specific for bes.nauru.lims
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """
