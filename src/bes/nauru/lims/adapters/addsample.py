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

from bika.lims import api
from bika.lims import senaiteMessageFactory as _s
from bika.lims.adapters.addsample import AddSampleObjectInfoAdapter
from bika.lims.catalog import SETUP_CATALOG
from bika.lims.interfaces import IAddSampleRecordsValidator
from bika.lims.interfaces import IGetDefaultFieldValueARAddHook
from bika.lims.utils import get_client
from bes.nauru.lims import logger
from bes.nauru.lims import messageFactory as _
from bes.nauru.lims.utils import get_field_value
from bes.nauru.lims.utils import to_localized_time
from senaite.core.api import measure as mapi
from zope.component import adapter
from zope.interface import implementer


@implementer(IAddSampleRecordsValidator)
class RecordsValidator(object):
    """Add Sample form records validator
    """

    def __init__(self, request):
        self.request = request

    def validate(self, records):
        """Returns None if all records are valid. Returns an error dict like
        follows otherwise, so the error messages it contains is displayed at
        the top of the Add Sample form view.
            {"message": "", "fielderrors": {}}
        """
        message = ""
        field_errors = {}
        for num, record in enumerate(records):

            # Check if volume is correct based on the selected sample type
            err = self.validate_minimum_volume(record)
            if err:
                field_errors["Volume-{}".format(num)] = err

            err = self.validate_maximum_volume(record)
            if err:
                field_errors["Volume-{}".format(num)] = err

            # Check Date of Admission is before or equal to the Date Sampled
            err = self.validate_date_of_admission(record)
            if err:
                field_errors["DateOfAdmission-{}".format(num)] = err

            # Specification is mandatory depending on sample type
            err = self.validate_specification(record)
            if err:
                field_errors["Specification-{}".format(num)] = err

        if any([message, field_errors]):
            return {
                "message": message,
                "fielderrors": field_errors
            }

    def validate_specification(self, record):
        """Returns an error message if no specification has been selected
        although required or the specification is not valid
        """
        spec_uid = record.get("Specification")
        if spec_uid:
            return None

        # specification required if a specification has been set up for the
        # selected sample type
        sample_type_uid = record.get("SampleType")
        query = {
            "portal_type": "AnalysisSpec",
            "sampletype_uid": sample_type_uid,
            "is_active": True,
        }
        specs = api.search(query, SETUP_CATALOG)
        if len(specs):
            return _("Specification is required")

    def validate_date_of_admission(self, record):
        """Validates the Date of Admission: before or equal to the Date Sampled
        """
        error = None
        # DateOfAdmission is an optional field in Add form, so we pass the
        # validation process if the record doesn't contain a DateOfAdmission
        date_of_admission = record.get("DateOfAdmission")

        if not date_of_admission:
            return error

        # DateSampled is a required field in Add form, so we can assume the
        # record contains a valid DateSampled value
        date_sampled = record.get("DateSampled")

        # Compare
        if date_of_admission > date_sampled:
            date_sampled = to_localized_time(date_sampled)
            error = _("Date of Admission must be equal or before Sampled Date "
                      "on {}").format(date_sampled)

        # Return the error (if any)
        return error

    def validate_minimum_volume(self, record):
        """Validates the Volume set in the record is above the minimum volume
        required for the selected sample type
        """
        error = None

        # SampleType is a required field in Add form, so we can assume the
        # record contains a valid uid value
        sample_type_uid = record.get("SampleType")
        sample_type = api.get_object(sample_type_uid)

        # Minimum volume required for the selected sample type
        min_volume_str = sample_type.getMinimumVolume() or None

        # Volume set by the user
        volume_str = record.get("Volume", None)

        # Convert to magnitude for proper comparison
        min_volume = mapi.get_magnitude(min_volume_str, default="0ml")
        volume = mapi.get_magnitude(volume_str, default="0ml")

        # Compare
        if volume < min_volume:
            error = _("Volume is below {}").format(min_volume_str)
            if not volume_str:
                error = _s("Field '{}' is required").format("Volume")

        # Return the error (if any)
        return error

    def validate_maximum_volume(self, record):
        """Validates the Volume set in the record is above the maximum volume
        required for the selected sample type
        """
        error = None

        # SampleType is a required field in Add form, so we can assume the
        # record contains a valid uid value
        sample_type_uid = record.get("SampleType")
        sample_type = api.get_object(sample_type_uid)

        # Maximum volume required for the selected sample type
        max_volume_str = sample_type.getMaximumVolume()
        if not max_volume_str:
            # No max volume set for this sample type, nothing to validate
            return

        if not mapi.is_volume(max_volume_str):
            # this should never happen. This value should have been validated
            # on sample type form submission
            logger.warn("Sample type has not a valid max volume: {}".format(
                max_volume_str
            ))
            return

        # Volume set by the user
        volume_str = record.get("Volume", None)

        # Convert to magnitude for proper comparison
        max_volume = mapi.get_magnitude(max_volume_str)
        volume = mapi.get_magnitude(volume_str, default="0ml")

        # Compare
        if volume > max_volume:
            error = _("Volume is over {}").format(max_volume_str)
            if not volume_str:
                error = _s("Field '{}' is required").format("Volume")

        # Return the error (if any)
        return error


@adapter(IGetDefaultFieldValueARAddHook)
class ClientDefaultValue(object):
    """Adapter that returns the default value for field 'Client' in Add sample
    """

    def __init__(self, request):
        self.request = request

    def __call__(self, context):
        """Returns the default client object based on the contact the current
        user is linked to, but only if current context does not belong to an
        existing client
        """
        # Try first with the current client from context
        client = get_client(context)

        if not client:
            # Get the current user logged in
            user = api.get_current_user()

            # Get the contact this user is linked to, if any
            contact = api.get_user_contact(user, contact_types=["LabContact"])
            if contact:
                client = get_field_value(contact, "DefaultClient")

        return client


@adapter(IGetDefaultFieldValueARAddHook)
class PrimaryAnalysisRequestDefaultValue(object):
    """Adapter that returns the default value for field
    'PrimaryAnalysisRequest' in Add sample form
    """

    def __init__(self, request):
        self.request = request

    def __call__(self, context):
        """Returns the default sample to be assigned to the current sample
        """
        request = api.get_request()

        # Extract the UIDs of primaries embedded in the request
        original_primaries = request.get("primary", "")
        primaries = request.get("_primary", original_primaries)

        # Remove non-uids just in case
        primaries = filter(api.is_uid, primaries.split(","))
        if not primaries:
            return

        # Pick the last object of the list
        primary = api.get_object_by_uid(primaries[-1])

        # And overwrite the value from request
        request["_primary"] = ",".join(primaries[:-1])

        return primary


class AddSampleTypeInfo(AddSampleObjectInfoAdapter):
    """Returns the additional filter queries to apply when the value for the
    SampleType for Sample Add form changes
    """

    def get_object_info(self):
        object_info = self.get_base_info()
        uid = api.get_uid(self.context)

        # If there is only one specification assigned to this sample type,
        # auto-choose that specification
        query = {
            "portal_type": "AnalysisSpec",
            "sampletype_uid": uid,
            "is_active": True,
        }
        specs = api.search(query, SETUP_CATALOG)
        if len(specs) == 1:
            obj = api.get_object(specs[0])
            object_info["field_values"]["Specification"] = {
                "id": api.get_id(obj),
                "uid": api.get_uid(obj),
                "url": api.get_url(obj),
                "title": api.get_title(obj),
                "if_empty": True,
            }

        return object_info
