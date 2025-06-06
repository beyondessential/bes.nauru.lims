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

from bes.nauru.lims import messageFactory as _
from Products.Archetypes import DisplayList

UNKNOWN_DOCTOR_FULLNAME = "Unknown doctor"

LANG_SETTINGS = [
    # Site language
    ("default_language", "en"),
    # Available languages
    ("available_languages", ["en", "na"]),
    # Show country-specific language variants
    # IMPORTANT: If True, .pot files for language variants are required
    ("use_combined_language_codes", False),
]

SETUP_SETTINGS = [
    ("title", "Setup"),
    # Security
    ("RestrictWorksheetUsersAccess", True),
    ("AllowToSubmitNotAssigned", True),
    ("RestrictWorksheetManagement", True),
    # Enable global Audit Log
    ("EnableGlobalAuditlog", False),
    # Accounting
    ("ShowPrices", False),
    ("Currency", "AUD"),
    ("DefaultCountry", "NR"),
    ("MemberDiscount", "0"),
    ("VAT", "10"),
    # Analyses
    ("CategoriseAnalysisServices", True),
    ("CategorizeSampleAnalyses", True),
    ("SampleAnalysesRequired", True),
    ("ExponentialFormatThreshold", "5"),
    ("EnableAnalysisRemarks", True),
    ("AutoVerifySamples", True),
    ("DefaultNumberOfARsToAdd", "1"),
    ("MaxNumberOfSamplesAdd", "10"),
    # Appearance
    ("ShowPartitions", True),
    # Sampling
    ("AutoreceiveSamples", True),
    # Sticker
    ("AutoPrintStickers", "receive"),
    ("DefaultNumberOfCopies", "3"),
    ("AutoStickerTemplate", "bes.nauru.lims.stickers:Code_39_40x20mm"),
    ("SmallStickerTemplate", "bes.nauru.lims.stickers:QR_1x14mmx39mm"),
    ("LargeStickerTemplate", "bes.nauru.lims.stickers:Code_39_40x20mm"),
]

LABORATORY_ADDRESS = {
    "address": "",
    "zip": "",
    "city": "",
    "district": "",
    "state": "",
    "country": "Nauru",
}

LABORATORY_SETTINGS = [
    ("title", "Laboratory"),
    ("Name", "Laboratory"),
    ("PhysicalAddress", LABORATORY_ADDRESS),
    ("PostalAddress", LABORATORY_ADDRESS),
    ("BillingAddress", LABORATORY_ADDRESS),
    ("Phone", ""),
    ("Fax", ""),
    ("EmailAddress", ""),
    ("LabURL", ""),
]

IMPRESS_SETTINGS = [
    ("templates", ["bes.nauru.lims.impress:Default.pt", ]),
    ("default_template", "bes.nauru.lims.impress:Default.pt"),
]

PATIENT_SETTINGS = [
    ("senaite.patient.gender_visible", False),
    ("senaite.patient.age_supported", False),
    ("senaite.patient.patient_entry_mode", "first_last"),
]

REJECTION_REASONS = (
    "Unsuitable specimen container",
    "Insufficient specimen collected",
    "Specimen contaminated",
    "Labelling error",
    "Unlabelled",
    "Specimen received in syringe",
    "No specimen received",
    "No lab request form",
    "Leakage during transit",
    "Please recollect if clinically indicated",
)

# Tuples of (id, folder_id)
# If folder_id is None, assume folder_id is portal
ACTIONS_TO_HIDE = [
]

# An array of dicts. Each dict represents an ID formatting configuration
ID_FORMATTING = [
    {
        "portal_type": "AnalysisRequest",
        "form": "{clientId}{sampleType}{year}{alpha:1a3d}",
        "prefix": "analysisrequest",
        "sequence_type": "generated",
        # Split length is the number of elements to join without taking the
        # 'separator' (default '-') into account. Thus, for a format like
        # AR-{sampleType}-{parentId}{alpha:3a2d}, the suitable split_length
        # should be 3, so the parts "AR", "{sampleType}" and "{parentId}" are
        # joined together as the prefix template ("AR-{sampleType}{parentId}",
        # so the last part ({alpha:3a2d}) becomes computed each time.
        "split_length": 3,
    }, {
        "portal_type": "AnalysisRequestPartition",
        "form": "{parent_ar_id}P{partition_count:01d}",
        "prefix": "analysisrequestpartition",
        "sequence_type": "",
        "split-length": 1
    }, {
        "portal_type": "AnalysisRequestRetest",
        "form": "{parent_base_id}R{retest_count:01d}",
        "prefix": "analysisrequestretest",
        "sequence_type": "",
        "split-length": 1
    }, {
        "portal_type": "AnalysisRequestSecondary",
        "form": "{parent_ar_id}S{secondary_count:01d}",
        "prefix": "analysisrequestsecondary",
        "sequence_type": "",
        "split-length": 1
    }, {
        "portal_type": "Worksheet",
        "form": "WS{yymmdd}-{seq:02d}",
        "prefix": "worksheet",
        "sequence_type": "generated",
        "split_length": 2,
    }, {
        "portal_type": "MedicalRecordNumber",
        "form": "TA{seq:06d}",
        "prefix": "medicalrecordnumber",
        "sequence_type": "generated",
        "split_length": 1,
    }
]

# List of field names to not display in Sample Add form
SAMPLE_ADD_FIELDS_TO_HIDE = [
    "CCContact",
    "CCEmails",
    "Batch",
    "InternalUse",
    "Preservation",
    "SampleCondition",
    "DateOfAdmission",
    "PatientAddress",
    "Template",
    "EnvironmentalConditions",
    "Preservation",
    "SamplingDate",
    "SamplePoint",
]

# Display order of Sample fields
SAMPLE_FIELDS_ORDER = [
    "PrimaryAnalysisRequest",
    "Batch",
    "Client",
    "Contact",
    "CCContact",
    "CCEmails",
    "MedicalRecordNumber",
    "PatientFullName",
    "PatientAddress",
    "DateOfBirth",
    "Sex",
    "Gender",
    "SamplingDate",
    "DateSampled",
    "DateOfAdmission",
    "WardDepartment",
    "Ward",
    "Location",
    "ClinicalInformation",
    "CurrentAntibiotics",
    "SampleType",
    "SampleCondition",
    "Profiles",
    "Template",
    "Container",
    "Bottles",
    "Preservation",
    "Volume",
    "SamplePoint",
    "EnvironmentalConditions",
    "Priority",
    "InternalUse",
    "RejectionReasons",
    "Remarks",
    "_ARAttachment",
    "NumSamples",
    "Specification",
]

LOCATIONS = DisplayList((
    ("int", _("Inpatient")),
    ("out", _("Outpatient")),
    ("ref", _("Referral")),
    ("img", _("Immigration")),
    ("", _("Not specified")),
))

PRIORITIES = DisplayList((
    ("1", _("Urgent")),
    ("5", _("Routine")),
))
