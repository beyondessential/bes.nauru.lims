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

from bika.lims.api import security
from bes.nauru.lims.utils import is_unknown_doctor
from Products.CMFCore.permissions import ModifyPortalContent


def AfterTransitionEventHandler(contact, event):  # noqa camelcase
    """Actions to be done when a transition for a contact takes place.
    If the contact is an Unknown doctor, ensures the contact cannot be modified
    """
    if not event.transition:
        return

    if not is_unknown_doctor(contact):
        return

    # Do not allow the modification of this contact
    roles = security.get_valid_roles_for(contact)
    security.revoke_permission_for(contact, ModifyPortalContent, roles)
