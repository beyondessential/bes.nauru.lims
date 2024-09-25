# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

from bes.nauru.lims.utils import contains_ast_analyses
from bes.nauru.lims.utils import contains_microorganism_identification_test


def available(self):
    """Returns true if senaite.ast is installed
    """
    if contains_ast_analyses(self.context):
        return True
    if contains_microorganism_identification_test(self.context):
        return True
    return False
