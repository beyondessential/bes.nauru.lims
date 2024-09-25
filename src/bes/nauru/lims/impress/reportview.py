# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

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
