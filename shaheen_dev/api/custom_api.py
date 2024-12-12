import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def update_student_progress(student_id, checked_fields):
    if not student_id:
        frappe.throw(("Please select a student first."))

    # Convert checked_fields from JSON string to a Python list
    checked_fields = frappe.parse_json(checked_fields)

    # Get the current date to be used for the date fields
    current_date = nowdate()

    # Define the date fields that correspond to each checkbox
    date_fields = {
        'ghusol_farayez': 'date_of_farayez_ghusol',
        'ghusol_sunath': 'date_of_sunath_ghusol',
        'ghusol_nawaqis': 'date_of_nawaqis_ghusol',
        'wazu_farayez': 'date_of_farayez_wazu',
        'wazu_sunath': 'date_of_sunath_wazu',
        'wazu_nawaqis': 'date_of_nawaqis_wazu',
        'sharayath_e_tayammum': 'date_of_sharayath_e_tayammum',
        'faraez_e_tayammum': 'date_of_faraez_e_tayammum',
        'nawaqis_e_tayammum': 'date_of_nawaqis_e_tayammum',
        'fajar': 'date_of_fajar_namaz',
        'zohar': 'date_of_zohar_namaz',
        'asar': 'date_of_asar_namaz',
        'magrib': 'date_of_magrib_namaz',
        'isha': 'date_of_isha_namaz',
        'juma': 'date_of_juma_namaz',
        'fraez_e_namaz': 'date_of_fraez',
        'wajibath_e_namaz': 'date_of_wajibath',
        'sana': 'date_of_sana',
        'sureh_fatihah': 'date_of_sureh_fatihah',
        'surah_e_feel': 'date_of_surah_e_feel',
        'surah_e_iqlas': 'date_of_surah_e_iqlas',
        'surah_e_falaq': 'date_of_surah_e_falaq',
        'surah_e_nas': 'date_of_surah_e_nas',
        'tasbihath_rukh_and_sajda': 'date_of_tasbihath_rukh_and_sajda',
        'attahiyath': 'date_of_attahiyath',
        'darood_e_ibrahim': 'date_of_darood_e_ibrahim',
        'duwa_e_masora': 'date_of_duwa_e_masora',
        'from_sana_to_salam': 'date_of_sana_to_salam',
        'sana_to_salam': 'date_of_sana_to_salam_',
        'duwa_balig_mard_ya_aurath': 'date_of_duwa_balig_mard_ya_aurath',
        'duwa_nabalig_bacha': 'date_of_nabalig_bacha',
        'duwa_nabalig_bachi': 'date_of_nabalig_bachi'
    }

    # Fetch the Student Complete Progress document or create a new one if not found
    student_progress = frappe.get_all('Student Complete Progress', filters={'student_name': student_id}, limit=1)

    if student_progress:
        student_progress = frappe.get_doc('Student Complete Progress', student_progress[0].name)
    else:
        # Create a new Student Complete Progress document
        student_progress = frappe.get_doc({
            'doctype': 'Student Complete Progress',
            'student_name': student_id
        })
        student_progress.insert()
        # frappe.msgprint(("A new Student Complete Progress record has been created for this student."))

    # Update the checked fields
    updated_fields = []
    for field in checked_fields:
        # Get the corresponding date field for each checked field
        date_field = date_fields.get(field)
        
        if date_field:
            # If we have a valid date field, update it
            if getattr(student_progress, field, False) != True:  # Only update if it's not already checked
                setattr(student_progress, field, True)
                setattr(student_progress, date_field, current_date)
                updated_fields.append(field)

    if updated_fields:
        student_progress.save()
        frappe.db.commit()

        return {
            'message': 'Student progress updated successfully.',
            'updated_fields': updated_fields
        }
    else:
        return {
            'message': 'No fields were updated.',
            'updated_fields': []
        }


@frappe.whitelist()
def fetch_student_progress(student_id):
    # Fetch the student progress from Student Complete Progress
    student_progress = frappe.get_all('Student Complete Progress', filters={'student_name': student_id}, limit=1)

    if student_progress:
        print("triggered")        
        student_progress = frappe.get_doc('Student Complete Progress', student_progress[0].name)
        return student_progress.as_dict()
    else:
        return {}


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



