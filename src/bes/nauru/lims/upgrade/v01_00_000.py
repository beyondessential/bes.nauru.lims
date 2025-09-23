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

from bes.nauru.lims import logger
from bes.nauru.lims import PRODUCT_NAME as product
from bes.nauru.lims.setuphandlers import update_ast_self_verification
from bika.lims import api
from senaite.core.catalog import ANALYSIS_CATALOG
from senaite.core.upgrade import upgradestep
from senaite.core.upgrade.utils import UpgradeUtils

version = "1.0.0"  # Remember version number in metadata.xml and setup.py
profile = "profile-{0}:default".format(product)


@upgradestep(product, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(product)

    if ut.isOlderVersion(product, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            product, ver_from, version))
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(product, ver_from, version))

    # -------- ADD YOUR STUFF BELOW --------

    logger.info("{0} upgraded to version {1}".format(product, version))
    return True


def enable_ast_self_verification(tool):
    """Enables the self-verification of ast-like services and analyses
    """
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup

    # Enable self-verification of ast-like services
    update_ast_self_verification(portal)

    # Enable self-verification of ast-like analyses
    logger.info("Setup self-verification of AST analyses ...")
    statuses = ["registered", "unassigned", "assigned", "to_be_verified"]
    query = {
        "portal_type": "Analysis",
        "review_state": statuses,
    }
    brains = api.search(query, ANALYSIS_CATALOG)
    for brain in brains:
        try:
            analysis = api.get_object(brain, default=None)
        except AttributeError:
            analysis = None

        if not analysis:
            continue

        logger.info("Enabling self-verification of %r" % analysis)
        analysis.setSelfVerification(1)

        # Flush the object from memory
        analysis._p_deactivate()

    logger.info("Setup self-verification of AST analyses [DONE]")
