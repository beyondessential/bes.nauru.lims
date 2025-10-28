# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS.
#
# BES.NAURU.LIMS is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
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
# Copyright 2023-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from bes.nauru.lims.astm import ASTMBaseImporter as Base


KEYWORDS_MAPPING = (
    # Tuple of (cobas c 311 analyzer Host Test No., (service_keywords))
    ("413", ["Alb"]),
)


class ASTMImporter(Base):
    """Results importer for Roche Cobas c 311
    """

    @property
    def keywords_mapping(self):
        return dict(KEYWORDS_MAPPING)

    def get_patient(self):
        patients = self.get_patients()
        if len(patients) != 1:
            return {}
        return patients[0]

    def get_sample_id(self, default=None):
        """Get the Sample ID
        """
        sample = super(ASTMImporter, self).get_sample_id(default=default)
        if not sample:
            return default

        if api.is_string(sample):
            # this is the sample id as described in the docs
            return sample.strip()

        # This field behaves different from what is described in the docs. It
        # should be a single string, but is a component of 5 fields
        sample_id = sample.get("sample_id")
        if api.is_string(sample_id):
            return sample_id.strip()

        return default

    def get_test_id(self, record):
        """Returns the test ID from the given results record
        """
        test = record.get("test") or {}
        # ^^^<ApplicationCode>/<Dilution>/<pre-dilution>/…
        #
        # <ApplicationCode> Type: NM Max: 5
        #   indicates cobas c 311 analyzer Host Test No.
        #   The analyzer identifies the test with 3-digit numbers. Specify
        #   these 3-digit numbers.
        #   The range of application code is expanded to 5-digit.
        #       Photometrics: 1-910,
        #       ISEs: Na=989, K=990, Cl=991
        #       Serum Index: L=992, H=993, I=994,
        #       Calculated Tests: 961-968
        #
        # <Dilution> Type: ST Max: 3
        #   Indicates automatic dilution factor when ordering.
        #   Inc, Dec,3,5,10,20,50
        #   When not specified, pipetting and testing is done using the
        #   standard analysis parameters
        application_code = test.get("application_code")

        # Ensure the dilution component is not considered
        application_code = application_code.split("/")[0]
        return application_code.strip()

    def get_captured_date(self, record):
        """Returns the date when the result was captured
        """
        return record.get("started_at")
