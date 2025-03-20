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

from bes.lims.impress.reportview import DefaultReportView as BaseView
from bika.lims import api


class DefaultReportView(BaseView):
    """Product-specific controller view for multiple results reports
    """

    def is_valid_status(self, analysis):
        """Returns whether the analysis object or brain is in a valid status
        """
        invalid = ["retracted", "rejected", "cancelled"]
        return api.get_review_status(analysis) not in invalid

    def is_results_in_progress(self, sample):
        """Returns true if there are analyses not yet verified
        """
        def in_progress(analysis):
            return not analysis.getDateVerified()

        # Exclude invalid analyses
        analyses = self.get_analyses(sample)
        analyses = filter(self.is_valid_status, analyses)

        # Ensure all valid analyses are in progress
        analyses = map(in_progress, analyses)
        return any(analyses)
