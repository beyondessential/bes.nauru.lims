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


from bes.nauru.lims import utils
from senaite.ast.browser.addpanel import AddPanelView as BaseView


class AddPanelView(BaseView):

    def __call__(self):
        # set the panel to current sample
        panel_uid = self.request.form.get("panel_uid")
        utils.set_ast_panel_to_sample(panel_uid, self.context)

        # return response from base class
        return super(AddPanelView, self).__call__()
