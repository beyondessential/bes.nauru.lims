# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bes.nauru.lims import messageFactory as _
from bes.nauru.lims.content import update_field
from bes.nauru.lims.interfaces import IBesNauruLimsLayer
from bika.lims import senaiteMessageFactory as _c
from bika.lims.interfaces import IBaseAnalysis
from Products.Archetypes import DisplayList
from zope.component import adapter
from zope.interface import implementer

# A tuple with (field_name, properties), where properties is a dict
UPDATED_FIELDS = [
    ("ResultOptions", {
        "subfields": ("ResultValue", "ResultText", "Flag"),
        "subfield_labels": {
            "ResultValue": _c("Result Value"),
            "ResultText": _c("Display Value"),
            "Flag": _("Flag"),
        },
        "subfield_types": {
            "Flag": "selection",
        },
        "subfield_sizes": {
            "Flag": 1,
        },
        "subfield_vocabularies": {
            "Flag": DisplayList((
                ('', ''),
                ('negative', _('Negative')),
                ('positive', _('Positive')),
            )),
        },
    }),
]


@adapter(IBaseAnalysis)
@implementer(ISchemaModifier, IBrowserLayerAwareExtender)
class BaseAnalysisSchemaModifier(object):
    layer = IBesNauruLimsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Update some fields (title, description, etc.)
        map(lambda f: update_field(schema, f[0], f[1]), UPDATED_FIELDS)
        return schema
