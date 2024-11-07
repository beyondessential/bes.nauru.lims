# -*- coding: utf-8 -*-
#
# This file is part of BES.NAURU.LIMS
#
# Copyright 2024 Beyond Essential Systems Pty Ltd

from bika.lims.api import get_portal
from bes.nauru.lims import logger
from bes.nauru.lims import PRODUCT_NAME
from bes.nauru.lims.setuphandlers import hide_actions
from bes.nauru.lims.setuphandlers import setup_behaviors
from bes.nauru.lims.setuphandlers import setup_catalogs
from bes.nauru.lims.setuphandlers import setup_workflows


def afterUpgradeStepHandler(event):  # noqa CamelCase
    """Event handler executed after running an upgrade step of senaite.core
    """

    logger.info("Run {}.afterUpgradeStepHandler ...".format(PRODUCT_NAME))
    portal = get_portal()
    setup = portal.portal_setup  # noqa

    profile = "profile-{0}:default".format(PRODUCT_NAME)
    setup.runImportStepFromProfile(profile, "typeinfo")
    setup.runImportStepFromProfile(profile, "rolemap")
    setup.runImportStepFromProfile(profile, "workflow")

    # Setup catalogs
    setup_catalogs(portal)

    # Add behaviors
    setup_behaviors(portal)

    # Setup workflows
    setup_workflows(portal)

    # Hide actions from both navigation portlet and from control_panel
    hide_actions(portal)

    logger.info("Run {}.afterUpgradeStepHandler [DONE]".format(PRODUCT_NAME))
