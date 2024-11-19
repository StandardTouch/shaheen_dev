import frappe
from frappe.utils import nowdate
import json

@frappe.whitelist()
def create_weekly_progress(student_id):
    """
    Fetch unchecked fields for the student and prepare data for creating a Weekly Student Progress document.
    """
    # Check if Student Complete Progress exists
    student_progress = frappe.db.get_value("Student Complete Progress", {"student_name": student_id}, "name")

    # If it doesn't exist, create a new document
    if not student_progress:
        student_progress = frappe.get_doc({
            "doctype": "Student Complete Progress",
            "student_name": student_id
        })
        student_progress.insert(ignore_permissions=True)
        frappe.db.commit()

    # Fetch the Student Complete Progress document
    student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

    unchecked_fields = []
    previously_checked_fields = {}
    previously_checked_dates = {}

    # Correct field-to-field mapping
    field_mapping = {
        "ghusol_farayez": "farayez_ghusol",
        "ghusol_sunath": "sunath_ghusol",
        "ghusol_nawaqis": "nawaqis_ghusol",
        "wazu_farayez": "farayez",
        "wazu_sunath": "sunath",
        "wazu_nawaqis": "nawaqis",
        "sharayath_e_tayammum": "sharayath_e_tayammum",
        "faraez_e_tayammum": "faraez_e_tayammum",
        "nawaqis_e_tayammum": "nawaqis_e_tayammum",
        "fajar": "fajar",
        "zohar": "zohar",
        "asar": "asar",
        "magrib": "magrib",
        "isha": "isha",
        "juma": "juma",
        "fraez_e_namaz": "fraez_e_namaz",
        "wajibath_e_namaz": "wajibath_e_namaz",
        "sana": "sana",
        "sureh_fatihah": "sureh_fatihah",
        "surah_e_feel": "zammi_surah",
        "surah_e_iqlas": "surah_e_iqlas",
        "surah_e_falaq": "surah_e_falaq",
        "surah_e_nas": "surah_e_nas",
        "tasbihath_rukh_and_sajda": "tasbihath_rukh_and_sajda",
        "attahiyath": "attahiyath",
        "darood_e_ibrahim": "darood_e_ibrahim",
        "duwa_e_masora": "duwa_e_masora",
        "from_sana_to_salam": "from_sana_to_salam",
        "sana_to_salam": "sana_to_salam",
        "duwa_balig_mard_ya_aurath": "duwa_balig_mard_ya_aurath",
        "duwa_nabalig_bacha": "duwa_nabalig_bacha",
        "duwa_nabalig_bachi": "duwa_nabalig_bachi",
    }

    # Correct date field mapping
    date_field_mapping = {
        "ghusol_farayez": "date_of_farayez_ghusol",
        "ghusol_sunath": "date_of_sunath_ghusol",
        "ghusol_nawaqis": "date_of_nawaqis_ghusol",
        "wazu_farayez": "date_of_farayez_wazu",
        "wazu_sunath": "date_of_sunath_wazu",
        "wazu_nawaqis": "date_of_nawaqis_wazu",
        "sharayath_e_tayammum": "date_of_sharayath_e_tayammum",
        "faraez_e_tayammum": "date_of_faraez_e_tayammum",
        "nawaqis_e_tayammum": "date_of_nawaqis_e_tayammum",
        "fajar": "date_of_fajar_namaz",
        "zohar": "date_of_zohar_namaz",
        "asar": "date_of_asar_namaz",
        "magrib": "date_of_magrib_namaz",
        "isha": "date_of_isha_namaz",
        "juma": "date_of_juma_namaz",
        "fraez_e_namaz": "date_of_fraez",
        "wajibath_e_namaz": "date_of_wajibath",
        "sana": "date_of_sana",
        "sureh_fatihah": "date_of_sureh_fatihah",
        "surah_e_feel": "date_of_surah_e_feel",
        "surah_e_iqlas": "date_of_surah_e_iqlas",
        "surah_e_falaq": "date_of_surah_e_falaq",
        "surah_e_nas": "date_of_surah_e_nas",
        "tasbihath_rukh_and_sajda": "date_of_tasbihath_rukh_and_sajda",
        "attahiyath": "date_of_attahiyath",
        "darood_e_ibrahim": "date_of_darood_e_ibrahim",
        "duwa_e_masora": "date_of_duwa_e_masora",
        "from_sana_to_salam": "date_of_sana_to_salam",
        "sana_to_salam": "date_of_sana_to_salam_",
        "duwa_balig_mard_ya_aurath": "date_of_duwa_balig_mard_ya_aurath",
        "duwa_nabalig_bacha": "date_of_nabalig_bacha",
        "duwa_nabalig_bachi": "date_of_nabalig_bachi",
    }

    # Fetch the fields to check
    fields_to_check = list(field_mapping.keys())

    for field in fields_to_check:
        if not student_progress.get(field):
            unchecked_fields.append(field_mapping[field])
        else:
            previously_checked_fields[field_mapping[field]] = 1
            previously_checked_dates[field_mapping[field]] = student_progress.get(date_field_mapping[field])

    return {
        "status": "success",
        "unchecked_fields": unchecked_fields,
        "previously_checked_fields": previously_checked_fields,
        "previously_checked_dates": previously_checked_dates,
        "student_id": student_id
    }

@frappe.whitelist()
def save_weekly_progress(student_id, field_data):
    """
    Save Weekly Progress Document with Field Data, ensuring Date Fields are populated, and submit it.
    """
    try:
        # Parse field_data to ensure it's a Python dictionary
        if isinstance(field_data, str):  # If field_data is a JSON string
            field_data = json.loads(field_data)

        # Fetch the student's complete progress
        student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

        # Correct field-to-date mapping
        field_to_date_mapping = {
            "nawaqis_ghusol": "date_of_nawaqis_ghusol",
            "farayez_ghusol": "date_of_farayez_ghusol",
            "sunath_ghusol": "date_of_sunath_ghusol",
            "farayez": "date_of_farayez",
            "sunath": "date_of_sunath",
            "nawaqis": "date_of_nawaqis",
            "sharayath_e_tayammum": "date_of_sharayath_e_tayammum",
            "faraez_e_tayammum": "date_of_faraez_e_tayammum",
            "nawaqis_e_tayammum": "date_of_nawaqis_e_tayammum",
            "fajar": "date_of_fajar_namaz",
            "zohar": "date_of_zohar_namaz",
            "asar": "date_of_asar_namaz",
            "magrib": "date_of_magrib_namaz",
            "isha": "date_of_isha_namaz",
            "juma": "date_of_juma_namaz",
            "fraez_e_namaz": "date_apdp",
            "wajibath_e_namaz": "date_of_wajibath",
            "sana": "date_of_sana",
            "sureh_fatihah": "date_of_sureh_fatihah",
            "zammi_surah": "date_of_surah_e_feel",
            "surah_e_iqlas": "date_of_surah_e_iqlas",
            "surah_e_falaq": "date_of_surah_e_falaq",
            "surah_e_nas": "date_of_surah_e_nas",
            "tasbihath_rukh_and_sajda": "date_of_tasbihath",
            "attahiyath": "date_of_attahiyath",
            "darood_e_ibrahim": "date_of_darood",
            "duwa_e_masora": "date_of_duwa_e_masora",
            "from_sana_to_salam": "date_of_sana_to_salam",
            "sana_to_salam": "date_of_sana_to_salam_",
            "duwa_balig_mard_ya_aurath": "date_of_duwa_balig_mard_ya_aurath",
            "duwa_nabalig_bacha": "date_of_nabalig_bacha",
            "duwa_nabalig_bachi": "date_of_nabalig_bachi",
        }

        # Prepare updated data
        updated_data = {}
        for field, value in field_data.items():
            if value:  # If checkbox is checked
                updated_data[field] = value  # Set the checkbox field

                # Fetch the corresponding date field
                date_field = field_to_date_mapping.get(field)
                if date_field:
                    # Fetch the date from Student Complete Progress or set today's date
                    updated_data[date_field] = student_progress.get(date_field) or nowdate()

        # Create the Weekly Student Progress document
        doc = frappe.get_doc({
            "doctype": "Weekly Student Progress",
            "student_id": student_id,
            **updated_data  # Include checkbox and date fields
        })

        # Insert the document
        doc.insert()

        # Submit the document
        doc.submit()

        return {
            "status": "success",
            "message": "Weekly progress saved and submitted successfully with dates populated.",
            "docname": doc.name
        }
    except Exception as e:
        # Log the error for debugging
        frappe.log_error(frappe.get_traceback(), "Error Saving and Submitting Weekly Progress")
        return {
            "status": "error",
            "message": str(e)
        }

def update_complete_progress(doc, method):
    """
    Update the Student Complete Progress document when a Weekly Student Progress document is created.
    """
    try:
        # Check if Student Complete Progress document exists for the student
        student_progress_name = frappe.db.get_value("Student Complete Progress", {"student_name": doc.student_id}, "name")

        # If it doesn't exist, create a new document
        if not student_progress_name:
            student_progress = frappe.get_doc({
                "doctype": "Student Complete Progress",
                "student_name": doc.student_id,
                # "student_name2": doc.student_id  # Use student_id as the name
            })
            student_progress.insert(ignore_permissions=True)
            student_progress_name = student_progress.name  # Fetch the generated name for further use

        # Fetch the existing Student Complete Progress document
        student_progress = frappe.get_doc("Student Complete Progress", student_progress_name)

        # Field mapping between Weekly Student Progress and Student Complete Progress
        field_mapping = {
            "farayez_ghusol": "ghusol_farayez",
            "sunath_ghusol": "ghusol_sunath",
            "nawaqis_ghusol": "ghusol_nawaqis",
            "farayez": "wazu_farayez",
            "sunath": "wazu_sunath",
            "nawaqis": "wazu_nawaqis",
            "sharayath_e_tayammum": "sharayath_e_tayammum",
            "faraez_e_tayammum": "faraez_e_tayammum",
            "nawaqis_e_tayammum": "nawaqis_e_tayammum",
            "fajar": "fajar",
            "zohar": "zohar",
            "asar": "asar",
            "magrib": "magrib",
            "isha": "isha",
            "juma": "juma",
            "fraez_e_namaz": "fraez_e_namaz",
            "wajibath_e_namaz": "wajibath_e_namaz",
            "sana": "sana",
            "sureh_fatihah": "sureh_fatihah",
            "zammi_surah": "surah_e_feel",
            "surah_e_iqlas": "surah_e_iqlas",
            "surah_e_falaq": "surah_e_falaq",
            "surah_e_nas": "surah_e_nas",
            "tasbihath_rukh_and_sajda": "tasbihath_rukh_and_sajda",
            "attahiyath": "attahiyath",
            "darood_e_ibrahim": "darood_e_ibrahim",
            "duwa_e_masora": "duwa_e_masora",
            "from_sana_to_salam": "from_sana_to_salam",
            "sana_to_salam": "sana_to_salam",
            "duwa_balig_mard_ya_aurath": "duwa_balig_mard_ya_aurath",
            "duwa_nabalig_bacha": "duwa_nabalig_bacha",
            "duwa_nabalig_bachi": "duwa_nabalig_bachi",
        }

        # Date field mapping
        date_field_mapping = {
            "ghusol_farayez": "date_of_farayez_ghusol",
            "ghusol_sunath": "date_of_sunath_ghusol",
            "ghusol_nawaqis": "date_of_nawaqis_ghusol",
            "wazu_farayez": "date_of_farayez_wazu",
            "wazu_sunath": "date_of_sunath_wazu",
            "wazu_nawaqis": "date_of_nawaqis_wazu",
            "sharayath_e_tayammum": "date_of_sharayath_e_tayammum",
            "faraez_e_tayammum": "date_of_faraez_e_tayammum",
            "nawaqis_e_tayammum": "date_of_nawaqis_e_tayammum",
            "fajar": "date_of_fajar_namaz",
            "zohar": "date_of_zohar_namaz",
            "asar": "date_of_asar_namaz",
            "magrib": "date_of_magrib_namaz",
            "isha": "date_of_isha_namaz",
            "juma": "date_of_juma_namaz",
            "fraez_e_namaz": "date_of_fraez",
            "wajibath_e_namaz": "date_of_wajibath",
            "sana": "date_of_sana",
            "sureh_fatihah": "date_of_sureh_fatihah",
            "surah_e_feel": "date_of_surah_e_feel",
            "surah_e_iqlas": "date_of_surah_e_iqlas",
            "surah_e_falaq": "date_of_surah_e_falaq",
            "surah_e_nas": "date_of_surah_e_nas",
            "tasbihath_rukh_and_sajda": "date_of_tasbihath_rukh_and_sajda",
            "attahiyath": "date_of_attahiyath",
            "darood_e_ibrahim": "date_of_darood_e_ibrahim",
            "duwa_e_masora": "date_of_duwa_e_masora",
            "from_sana_to_salam": "date_of_sana_to_salam",
            "sana_to_salam": "date_of_sana_to_salam_",
            "duwa_balig_mard_ya_aurath": "date_of_duwa_balig_mard_ya_aurath",
            "duwa_nabalig_bacha": "date_of_nabalig_bacha",
            "duwa_nabalig_bachi": "date_of_nabalig_bachi",
        }

        # Loop through the field mappings and update the target document
        for weekly_field, complete_field in field_mapping.items():
            if student_progress.meta.has_field(complete_field):
                # Update the checkbox field
                weekly_value = doc.get(weekly_field)
                if weekly_value:
                    student_progress.set(complete_field, 1)  # Check the field

                # Handle date fields
                date_field = date_field_mapping.get(weekly_field)
                if date_field and student_progress.meta.has_field(date_field):
                    # Populate the date only if the weekly field is checked
                    if weekly_value:
                        student_progress.set(date_field, nowdate())

        # Save the updated Student Complete Progress document
        student_progress.save(ignore_permissions=True)
        frappe.db.commit()

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error updating Student Complete Progress")
        frappe.throw(("An error occurred while updating the student's progress: ") + str(e))
