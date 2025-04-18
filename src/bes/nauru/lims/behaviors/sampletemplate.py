# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS.
#
# BES.NAURU.LIMS is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2024-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

from AccessControl import ClassSecurityInfo
from bika.lims import api
from bes.nauru.lims import messageFactory as _
from plone.app.textfield import IRichTextValue
from plone.app.textfield.widget import RichTextFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.core.api import measure as mapi
from senaite.core.interfaces import ISampleTemplate
from senaite.core.schema import RichTextField
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


@provider(IFormFieldProvider)
class IExtendedSampleTemplateBehavior(model.Schema):

    minimum_volume = schema.TextLine(
        title=_(u"MinimumVolume"),
        description=_(
            u"The minimum sample volume required for analysis eg. '10 ml'"
        ),
        default=u"0 ml",
    )

    directives.widget("insufficient_volume_text", RichTextFieldWidget)
    insufficient_volume_text = RichTextField(
        title=_(u"Auto-text for when there is not enough volume"),
        description=_(
            u"When there is not enough volume, the contents entered here "
            u"are automatically inserted in Results Interpretation after "
            u"Sample verification"
        ),
        required=False
    )

    @invariant
    def validate_minimum_volume(data):
        """Checks if the volume is valid
        """
        volume = data.minimum_volume
        if not volume:
            # not required
            return

        context = getattr(data, "__context__", None)
        if context and context.minimum_volume == volume:
            # nothing changed
            return

        if not mapi.is_volume(volume):
            raise Invalid(_("Not a valid volume"))


@implementer(IExtendedSampleTemplateBehavior)
@adapter(ISampleTemplate)
class ExtendedSampleTemplate(object):

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context

    @security.protected(permissions.View)
    def getMinimumVolume(self):
        accessor = self.context.accessor("minimum_volume")
        value = accessor(self.context)
        return api.to_utf8(value, default="")

    @security.protected(permissions.ModifyPortalContent)
    def setMinimumVolume(self, value):
        mutator = self.context.mutator("minimum_volume")
        mutator(self.context, api.safe_unicode(value))

    minimum_volume = property(getMinimumVolume, setMinimumVolume)

    @security.protected(permissions.View)
    def getInsufficientVolumeText(self):
        accessor = self.context.accessor("insufficient_volume_text")
        value = accessor(self.context)
        if IRichTextValue.providedBy(value):
            # Transforms the raw value to the output mimetype
            value = value.output_relative_to(self.context)
        return value

    @security.protected(permissions.ModifyPortalContent)
    def setInsufficientVolumeText(self, value):
        mutator = self.context.mutator("insufficient_volume_text")
        mutator(self.context, value)

    insufficient_volume_text = property(getInsufficientVolumeText,
                                        setInsufficientVolumeText)


def getMinimumVolume(self):
    behavior = IExtendedSampleTemplateBehavior(self)
    return behavior.getMinimumVolume()


def setMinimumVolume(self, value):
    behavior = IExtendedSampleTemplateBehavior(self)
    behavior.setMinimumVolume(value)


def getInsufficientVolumeText(self):
    behavior = IExtendedSampleTemplateBehavior(self)
    return behavior.getInsufficientVolumeText()


def setInsufficientVolumeText(self, value):
    behavior = IExtendedSampleTemplateBehavior(self)
    behavior.setInsufficientVolumeText(value)
