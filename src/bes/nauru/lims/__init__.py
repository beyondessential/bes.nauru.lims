# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

import logging

from bes.nauru.lims import permissions
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import ContentInit
from zope.i18nmessageid import MessageFactory

PRODUCT_NAME = "bes.nauru.lims"
PROFILE_ID = "profile-{}:default".format(PRODUCT_NAME)

# Defining a Message Factory for when this product is internationalized.
messageFactory = MessageFactory(PRODUCT_NAME)
_ = messageFactory

logger = logging.getLogger(PRODUCT_NAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    logger.info("*** Initializing BES NAURU LIMS Customization package ***")

    # Get the content types from this product
    types = listTypes(PRODUCT_NAME)
    content_types, constructors, ftis = process_types(types, PRODUCT_NAME)

    # Register each type with it's own Add permission
    # use "Add portal content" as default
    all_types = zip(content_types, constructors)
    for content_type, constructor in all_types:
        kind = "%s: Add %s" % (PRODUCT_NAME, content_type.portal_type)
        perm_name = "Add{}".format(content_type.portal_type)
        perm = getattr(permissions, perm_name, AddPortalContent)
        ContentInit(kind,
                    content_types=(content_type,),
                    permission=perm,
                    extra_constructors=(constructor, ),
                    fti=ftis,
                    ).initialize(context)
