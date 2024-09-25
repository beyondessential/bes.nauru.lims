# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bes.lims.extender.field import ExtBlobImageField
from bes.lims.extender.field import ExtStringField
from bes.nauru.lims import messageFactory as _
from bes.nauru.lims.interfaces import IBesNauruLimsLayer
from bika.lims.interfaces import IClient
from Products.Archetypes.Widget import ImageWidget
from Products.Archetypes.Widget import StringWidget
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
                "Logo to display in the header of results reports for this "
                "client"
            )
      ),
    ),

    ExtStringField(
        "Abbreviation",
        mode="rw",
        required=False,
        schemata="default",
        widget=StringWidget(
            label=_("Abbreviation"),
            description=_(
                "The abbreviation of the hospital"
            )
        )
    )

]


@adapter(IClient)
@implementer(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
class ClientSchemaExtender(object):
    """Extends Client content type with additional fields
    """
    layer = IBesNauruLimsLayer

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default_schemata = schematas["default"]
        idx = default_schemata.index("ClientID")
        abbreviation = default_schemata.pop(
            default_schemata.index("Abbreviation")
        )
        default_schemata.insert(idx + 1, abbreviation)

        schematas["default"] = default_schemata
        return schematas

    def getFields(self):
        return NEW_FIELDS
