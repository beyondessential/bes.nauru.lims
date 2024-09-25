# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bes.lims.extender.field import ExtBlobImageField
from bes.nauru.lims import messageFactory as _
from bes.nauru.lims.interfaces import IBesNauruLimsLayer
from bika.lims.interfaces import IBikaSetup
from Products.Archetypes.Widget import ImageWidget
from zope.component import adapter
from zope.interface import implementer

# New fields to be added to this type
NEW_FIELDS = [

    ExtBlobImageField(
        "ReportLogo",
        schemata="Results Reports",
        widget=ImageWidget(
            label=_("Report Logo"),
            description=_(
                "Logo to display in the header of results reports"
            )
        ),
    ),

]


@adapter(IBikaSetup)
@implementer(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
class LimsSetupSchemaExtender(object):
    """Extends Setup content type with additional fields
    """
    layer = IBesNauruLimsLayer

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return NEW_FIELDS
