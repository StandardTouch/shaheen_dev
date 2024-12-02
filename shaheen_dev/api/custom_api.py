# import frappe
# from frappe.utils import nowdate

# # Field Mapping
# field_mapping = {
#     "ghusol_farayez": "ghusol_farayez",
#     "ghusol_sunath": "ghusol_sunath",
#     "ghusol_nawaqis": "ghusol_nawaqis",
#     "wazu_farayez": "wazu_farayez",
#     "wazu_sunath": "wazu_sunath",
#     "wazu_nawaqis": "wazu_nawaqis",
#     "sharayath_e_tayammum": "sharayath_e_tayammum",
#     "faraez_e_tayammum": "faraez_e_tayammum",
#     "nawaqis_e_tayammum": "nawaqis_e_tayammum",
#     "fajar": "fajar",
#     "zohar": "zohar",
#     "asar": "asar",
#     "magrib": "magrib",
#     "isha": "isha",
#     "juma": "juma",
#     "fraez_e_namaz": "fraez_e_namaz",
#     "wajibath_e_namaz": "wajibath_e_namaz",
#     "sana": "sana",
#     "sureh_fatihah": "sureh_fatihah",
#     "surah_e_feel": "surah_e_feel",
#     "surah_e_iqlas": "surah_e_iqlas",
#     "surah_e_falaq": "surah_e_falaq",
#     "surah_e_nas": "surah_e_nas",
#     "tasbihath_rukh_and_sajda": "tasbihath_rukh_and_sajda",
#     "attahiyath": "attahiyath",
#     "darood_e_ibrahim": "darood_e_ibrahim",
#     "duwa_e_masora": "duwa_e_masora",
#     "from_sana_to_salam": "from_sana_to_salam",
#     "sana_to_salam": "sana_to_salam",
#     "duwa_balig_mard_ya_aurath": "duwa_balig_mard_ya_aurath",
#     "duwa_nabalig_bacha": "duwa_nabalig_bacha",
#     "duwa_nabalig_bachi": "duwa_nabalig_bachi",
# }

# # Date Field Mapping
# date_field_mapping = {
#     "ghusol_farayez": "date_of_farayez_ghusol",
#     "ghusol_sunath": "date_of_sunath_ghusol",
#     "ghusol_nawaqis": "date_of_nawaqis_ghusol",
#     "wazu_farayez": "date_of_farayez_wazu",
#     "wazu_sunath": "date_of_sunath_wazu",
#     "wazu_nawaqis": "date_of_nawaqis_wazu",
#     "sharayath_e_tayammum": "date_of_sharayath_e_tayammum",
#     "faraez_e_tayammum": "date_of_faraez_e_tayammum",
#     "nawaqis_e_tayammum": "date_of_nawaqis_e_tayammum",
#     "fajar": "date_of_fajar_namaz",
#     "zohar": "date_of_zohar_namaz",
#     "asar": "date_of_asar_namaz",
#     "magrib": "date_of_magrib_namaz",
#     "isha": "date_of_isha_namaz",
#     "juma": "date_of_juma_namaz",
#     "fraez_e_namaz": "date_of_fraez",
#     "wajibath_e_namaz": "date_of_wajibath",
#     "sana": "date_of_sana",
#     "sureh_fatihah": "date_of_sureh_fatihah",
#     "surah_e_feel": "date_of_surah_e_feel",
#     "surah_e_iqlas": "date_of_surah_e_iqlas",
#     "surah_e_falaq": "date_of_surah_e_falaq",
#     "surah_e_nas": "date_of_surah_e_nas",
#     "tasbihath_rukh_and_sajda": "date_of_tasbihath_rukh_and_sajda",
#     "attahiyath": "date_of_attahiyath",
#     "darood_e_ibrahim": "date_of_darood_e_ibrahim",
#     "duwa_e_masora": "date_of_duwa_e_masora",
#     "from_sana_to_salam": "date_of_sana_to_salam",
#     "sana_to_salam": "date_of_sana_to_salam_",
#     "duwa_balig_mard_ya_aurath": "date_of_duwa_balig_mard_ya_aurath",
#     "duwa_nabalig_bacha": "date_of_nabalig_bacha",
#     "duwa_nabalig_bachi": "date_of_nabalig_bachi",
# }

# # @frappe.whitelist()
# # def create_weekly_progress(student_id):
# #     # Fetch the "Student Complete Progress" document
# #     student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

# #     # Initialize lists for unchecked fields and previously checked fields
# #     unchecked_fields = []
# #     previously_checked_fields = {}
# #     previously_checked_dates = {}

# #     # Process fields using field mappings
# #     for field in field_mapping.keys():
# #         checkbox_value = student_progress.get(field)
# #         date_value = student_progress.get(date_field_mapping.get(field))

# #         if not checkbox_value:  # Field is not checked
# #             unchecked_fields.append(field_mapping[field])
# #         else:  # Field is checked
# #             previously_checked_fields[field_mapping[field]] = 1
# #             previously_checked_dates[field_mapping[field]] = date_value or nowdate()

# #     # Create "Weekly Student Progress"
# #     weekly_progress = frappe.get_doc({
# #         "doctype": "Weekly Student Progress",
# #         "student_id": student_id,
# #         **previously_checked_fields,  # Include checked fields
# #         **previously_checked_dates,  # Include their dates
# #     })
# #     weekly_progress.insert()
# #     frappe.db.commit()

# #     # Update the "Student Complete Progress" document
# #     for field in unchecked_fields:
# #         source_field = next(k for k, v in field_mapping.items() if v == field)
# #         student_progress.set(source_field, 1)  # Mark field as checked
# #         student_progress.set(date_field_mapping[source_field], nowdate())  # Set today's date

# #     student_progress.save()
# #     frappe.db.commit()

# #     return {"status": "success", "message": "Weekly Progress created and Complete Progress updated successfully."}

# @frappe.whitelist()
# def fetch_complete_progress(student_id):
#     # Check if the Student Complete Progress document exists
#     student_progress = frappe.db.exists("Student Complete Progress", {"student_name": student_id})

#     if not student_progress:
#         # If the document does not exist, create a new one
#         new_doc = frappe.get_doc({
#             "doctype": "Student Complete Progress",
#             "student_name": student_id,
#             # Initialize other fields if necessary
#         })
#         new_doc.insert()
#         frappe.db.commit()
#         student_progress = new_doc

#     else:
#         # Fetch the existing document
#         student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

#     # Prepare lists for unchecked fields and previously checked fields
#     unchecked_fields = []
#     previously_checked_fields = {}

#     for field in field_mapping.keys():
#         checkbox_value = student_progress.get(field)
#         if not checkbox_value:  # If field is unchecked
#             unchecked_fields.append(field_mapping[field])  # Add to unchecked fields
#         else:  # If field is checked
#             previously_checked_fields[field_mapping[field]] = 1  # Add to checked fields

#     return {
#         "status": "success",
#         "unchecked_fields": unchecked_fields,
#         "previously_checked_fields": previously_checked_fields,
#         "student_id": student_id
#     }


# @frappe.whitelist()
# def update_complete_progress(student_id, selected_fields):
#     selected_fields = frappe.parse_json(selected_fields)

#     # Fetch the Student Complete Progress document
#     student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

#     # Store the previous state of the updated fields
#     previous_state = {}
#     for field in selected_fields.keys():
#         if selected_fields[field]:
#             previous_state[field] = student_progress.get(field)

#     # Check if an Undo Log already exists for this student
#     undo_log_name = frappe.db.exists("Undo Log", {"student_name": student_id})

#     if undo_log_name:
#         # Update the existing Undo Log
#         undo_log = frappe.get_doc("Undo Log", undo_log_name)
#         undo_log.last_update_data = frappe.as_json(previous_state)
#         undo_log.save()
#     else:
#         # Create a new Undo Log
#         frappe.get_doc({
#             "doctype": "Undo Log",
#             "student_name": student_id,
#             "last_update_data": frappe.as_json(previous_state)
#         }).insert()

#     # Update the fields in Student Complete Progress
#     for field in selected_fields.keys():
#         if selected_fields[field]:
#             student_progress.set(field, 1)  # Check the field
#             student_progress.set(date_field_mapping[field], nowdate())  # Update the date

#     # Save the document
#     student_progress.save()
#     frappe.db.commit()

#     return {"status": "success", "message": "Selected fields updated successfully."}



# @frappe.whitelist()
# def undo_last_update(student_id):
#     try:
#         # Fetch the Undo Log entry
#         last_update_log = frappe.db.get_value(
#             "Undo Log",
#             {"student_name": student_id},
#             "last_update_data",
#             as_dict=True
#         )

#         if not last_update_log:
#             frappe.throw(f"No updates found to undo for Student ID: {student_id}")

#         # Parse the JSON data
#         last_update_data = frappe.parse_json(last_update_log.get("last_update_data"))

#         # Fetch the Student Complete Progress document
#         student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

#         # Undo the last update by restoring previous values
#         for field, value in last_update_data.items():
#             student_progress.set(field, value)

#             # If the checkbox is being unchecked, clear the date field
#             if value == 0:
#                 date_field = date_field_mapping.get(field)
#                 if date_field:
#                     student_progress.set(date_field, None)

#         # Save the reverted document
#         student_progress.save()
#         frappe.db.commit()

#         # Clear the undo log after successful revert
#         frappe.db.delete("Undo Log", {"student_name": student_id})

#         return {"status": "success", "message": "Last update undone successfully."}
#     except Exception as e:
#         frappe.logger().error(f"Error undoing last update for {student_id}: {e}")
#         return {"status": "error", "message": f"Failed to undo the last update: {e}"}


# ///////////////////////////////////////////

# import frappe
# from frappe.utils import nowdate
# import json

# @frappe.whitelist()
# def create_weekly_progress(student_id):
#     """
#     Fetch unchecked fields for the student and prepare data for creating a Weekly Student Progress document.
#     """
#     # Check if Student Complete Progress exists
#     student_progress = frappe.db.get_value("Student Complete Progress", {"student_name": student_id}, "name")

#     # If it doesn't exist, create a new document
#     if not student_progress:
#         student_progress = frappe.get_doc({
#             "doctype": "Student Complete Progress",
#             "student_name": student_id
#         })
#         student_progress.insert(ignore_permissions=True)
#         frappe.db.commit()

#     # Fetch the Student Complete Progress document
#     student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

#     unchecked_fields = []
#     previously_checked_fields = {}
#     previously_checked_dates = {}

#     # Correct field-to-field mapping
#     field_mapping = {
#         "ghusol_farayez": "farayez_ghusol",
#         "ghusol_sunath": "sunath_ghusol",
#         "ghusol_nawaqis": "nawaqis_ghusol",
#         "wazu_farayez": "farayez",
#         "wazu_sunath": "sunath",
#         "wazu_nawaqis": "nawaqis",
#         "sharayath_e_tayammum": "sharayath_e_tayammum",
#         "faraez_e_tayammum": "faraez_e_tayammum",
#         "nawaqis_e_tayammum": "nawaqis_e_tayammum",
#         "fajar": "fajar",
#         "zohar": "zohar",
#         "asar": "asar",
#         "magrib": "magrib",
#         "isha": "isha",
#         "juma": "juma",
#         "fraez_e_namaz": "fraez_e_namaz",
#         "wajibath_e_namaz": "wajibath_e_namaz",
#         "sana": "sana",
#         "sureh_fatihah": "sureh_fatihah",
#         "surah_e_feel": "zammi_surah",
#         "surah_e_iqlas": "surah_e_iqlas",
#         "surah_e_falaq": "surah_e_falaq",
#         "surah_e_nas": "surah_e_nas",
#         "tasbihath_rukh_and_sajda": "tasbihath_rukh_and_sajda",
#         "attahiyath": "attahiyath",
#         "darood_e_ibrahim": "darood_e_ibrahim",
#         "duwa_e_masora": "duwa_e_masora",
#         "from_sana_to_salam": "from_sana_to_salam",
#         "sana_to_salam": "sana_to_salam",
#         "duwa_balig_mard_ya_aurath": "duwa_balig_mard_ya_aurath",
#         "duwa_nabalig_bacha": "duwa_nabalig_bacha",
#         "duwa_nabalig_bachi": "duwa_nabalig_bachi",
#     }

#     # Correct date field mapping
#     date_field_mapping = {
#         "ghusol_farayez": "date_of_farayez_ghusol",
#         "ghusol_sunath": "date_of_sunath_ghusol",
#         "ghusol_nawaqis": "date_of_nawaqis_ghusol",
#         "wazu_farayez": "date_of_farayez_wazu",
#         "wazu_sunath": "date_of_sunath_wazu",
#         "wazu_nawaqis": "date_of_nawaqis_wazu",
#         "sharayath_e_tayammum": "date_of_sharayath_e_tayammum",
#         "faraez_e_tayammum": "date_of_faraez_e_tayammum",
#         "nawaqis_e_tayammum": "date_of_nawaqis_e_tayammum",
#         "fajar": "date_of_fajar_namaz",
#         "zohar": "date_of_zohar_namaz",
#         "asar": "date_of_asar_namaz",
#         "magrib": "date_of_magrib_namaz",
#         "isha": "date_of_isha_namaz",
#         "juma": "date_of_juma_namaz",
#         "fraez_e_namaz": "date_of_fraez",
#         "wajibath_e_namaz": "date_of_wajibath",
#         "sana": "date_of_sana",
#         "sureh_fatihah": "date_of_sureh_fatihah",
#         "surah_e_feel": "date_of_surah_e_feel",
#         "surah_e_iqlas": "date_of_surah_e_iqlas",
#         "surah_e_falaq": "date_of_surah_e_falaq",
#         "surah_e_nas": "date_of_surah_e_nas",
#         "tasbihath_rukh_and_sajda": "date_of_tasbihath_rukh_and_sajda",
#         "attahiyath": "date_of_attahiyath",
#         "darood_e_ibrahim": "date_of_darood_e_ibrahim",
#         "duwa_e_masora": "date_of_duwa_e_masora",
#         "from_sana_to_salam": "date_of_sana_to_salam",
#         "sana_to_salam": "date_of_sana_to_salam_",
#         "duwa_balig_mard_ya_aurath": "date_of_duwa_balig_mard_ya_aurath",
#         "duwa_nabalig_bacha": "date_of_nabalig_bacha",
#         "duwa_nabalig_bachi": "date_of_nabalig_bachi",
#     }

#     # Fetch the fields to check
#     fields_to_check = list(field_mapping.keys())

#     for field in fields_to_check:
#         if not student_progress.get(field):
#             unchecked_fields.append(field_mapping[field])
#         else:
#             previously_checked_fields[field_mapping[field]] = 1
#             previously_checked_dates[field_mapping[field]] = student_progress.get(date_field_mapping[field])

#     return {
#         "status": "success",
#         "unchecked_fields": unchecked_fields,
#         "previously_checked_fields": previously_checked_fields,
#         "previously_checked_dates": previously_checked_dates,
#         "student_id": student_id
#     }

# @frappe.whitelist()
# def save_weekly_progress(student_id, field_data):
#     """
#     Save Weekly Progress Document with Field Data, ensuring Date Fields are populated, and submit it.
#     """
#     try:
#         # Parse field_data to ensure it's a Python dictionary
#         if isinstance(field_data, str):  # If field_data is a JSON string
#             field_data = json.loads(field_data)

#         # Fetch the student's complete progress
#         student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

#         # Correct field-to-date mapping
#         field_to_date_mapping = {
#             "nawaqis_ghusol": "date_of_nawaqis_ghusol",
#             "farayez_ghusol": "date_of_farayez_ghusol",
#             "sunath_ghusol": "date_of_sunath_ghusol",
#             "farayez": "date_of_farayez",
#             "sunath": "date_of_sunath",
#             "nawaqis": "date_of_nawaqis",
#             "sharayath_e_tayammum": "date_of_sharayath_e_tayammum",
#             "faraez_e_tayammum": "date_of_faraez_e_tayammum",
#             "nawaqis_e_tayammum": "date_of_nawaqis_e_tayammum",
#             "fajar": "date_of_fajar_namaz",
#             "zohar": "date_of_zohar_namaz",
#             "asar": "date_of_asar_namaz",
#             "magrib": "date_of_magrib_namaz",
#             "isha": "date_of_isha_namaz",
#             "juma": "date_of_juma_namaz",
#             "fraez_e_namaz": "date_apdp",
#             "wajibath_e_namaz": "date_of_wajibath",
#             "sana": "date_of_sana",
#             "sureh_fatihah": "date_of_sureh_fatihah",
#             "zammi_surah": "date_of_surah_e_feel",
#             "surah_e_iqlas": "date_of_surah_e_iqlas",
#             "surah_e_falaq": "date_of_surah_e_falaq",
#             "surah_e_nas": "date_of_surah_e_nas",
#             "tasbihath_rukh_and_sajda": "date_of_tasbihath",
#             "attahiyath": "date_of_attahiyath",
#             "darood_e_ibrahim": "date_of_darood",
#             "duwa_e_masora": "date_of_duwa_e_masora",
#             "from_sana_to_salam": "date_of_sana_to_salam",
#             "sana_to_salam": "date_of_sana_to_salam_",
#             "duwa_balig_mard_ya_aurath": "date_of_duwa_balig_mard_ya_aurath",
#             "duwa_nabalig_bacha": "date_of_nabalig_bacha",
#             "duwa_nabalig_bachi": "date_of_nabalig_bachi",
#         }

#         # Prepare updated data
#         updated_data = {}
#         for field, value in field_data.items():
#             if value:  # If checkbox is checked
#                 updated_data[field] = value  # Set the checkbox field

#                 # Fetch the corresponding date field
#                 date_field = field_to_date_mapping.get(field)
#                 if date_field:
#                     # Fetch the date from Student Complete Progress or set today's date
#                     updated_data[date_field] = student_progress.get(date_field) or nowdate()

#         # Create the Weekly Student Progress document
#         doc = frappe.get_doc({
#             "doctype": "Weekly Student Progress",
#             "student_id": student_id,
#             **updated_data  # Include checkbox and date fields
#         })

#         # Insert the document
#         doc.insert()

#         # Submit the document
#         doc.submit()
#         frappe.db.commit()


#         return {
#             "status": "success",
#             "message": "Weekly progress saved and submitted successfully with dates populated.",
#             "docname": doc.name
#         }
#     except Exception as e:
#         # Log the error for debugging
#         frappe.log_error(frappe.get_traceback(), "Error Saving and Submitting Weekly Progress")
#         return {
#             "status": "error",
#             "message": str(e)
#         }


# def update_complete_progress(doc, method):
#     """
#     Update the Student Complete Progress document when a Weekly Student Progress document is created.
#     """
#     try:
#         # Check if Student Complete Progress document exists for the student
#         student_progress_name = frappe.db.get_value("Student Complete Progress", {"student_name": doc.student_id}, "name")

#         # If it doesn't exist, create a new document
#         if not student_progress_name:
#             student_progress = frappe.get_doc({
#                 "doctype": "Student Complete Progress",
#                 "student_name": doc.student_id,
#             })
#             student_progress.insert(ignore_permissions=True)
#             student_progress_name = student_progress.name

#         # Fetch the existing Student Complete Progress document
#         student_progress = frappe.get_doc("Student Complete Progress", student_progress_name)

#         # Field mapping between Weekly Student Progress and Student Complete Progress
#         field_mapping = {
#             "farayez_ghusol": "ghusol_farayez",
#             "sunath_ghusol": "ghusol_sunath",
#             "nawaqis_ghusol": "ghusol_nawaqis",
#             "farayez": "wazu_farayez",
#             "sunath": "wazu_sunath",
#             "nawaqis": "wazu_nawaqis",
#             "sharayath_e_tayammum": "sharayath_e_tayammum",
#             "faraez_e_tayammum": "faraez_e_tayammum",
#             "nawaqis_e_tayammum": "nawaqis_e_tayammum",
#             "fajar": "fajar",
#             "zohar": "zohar",
#             "asar": "asar",
#             "magrib": "magrib",
#             "isha": "isha",
#             "juma": "juma",
#             "fraez_e_namaz": "fraez_e_namaz",
#             "wajibath_e_namaz": "wajibath_e_namaz",
#             "sana": "sana",
#             "sureh_fatihah": "sureh_fatihah",
#             "zammi_surah": "surah_e_feel",
#             "surah_e_iqlas": "surah_e_iqlas",
#             "surah_e_falaq": "surah_e_falaq",
#             "surah_e_nas": "surah_e_nas",
#             "tasbihath_rukh_and_sajda": "tasbihath_rukh_and_sajda",
#             "attahiyath": "attahiyath",
#             "darood_e_ibrahim": "darood_e_ibrahim",
#             "duwa_e_masora": "duwa_e_masora",
#             "from_sana_to_salam": "from_sana_to_salam",
#             "sana_to_salam": "sana_to_salam",
#             "duwa_balig_mard_ya_aurath": "duwa_balig_mard_ya_aurath",
#             "duwa_nabalig_bacha": "duwa_nabalig_bacha",
#             "duwa_nabalig_bachi": "duwa_nabalig_bachi",
#         }

#         # Date field mapping
#         date_field_mapping = {
#             "ghusol_farayez": "date_of_farayez_ghusol",
#             "ghusol_sunath": "date_of_sunath_ghusol",
#             "ghusol_nawaqis": "date_of_nawaqis_ghusol",
#             "wazu_farayez": "date_of_farayez_wazu",
#             "wazu_sunath": "date_of_sunath_wazu",
#             "wazu_nawaqis": "date_of_nawaqis_wazu",
#             "sharayath_e_tayammum": "date_of_sharayath_e_tayammum",
#             "faraez_e_tayammum": "date_of_faraez_e_tayammum",
#             "nawaqis_e_tayammum": "date_of_nawaqis_e_tayammum",
#             "fajar": "date_of_fajar_namaz",
#             "zohar": "date_of_zohar_namaz",
#             "asar": "date_of_asar_namaz",
#             "magrib": "date_of_magrib_namaz",
#             "isha": "date_of_isha_namaz",
#             "juma": "date_of_juma_namaz",
#             "fraez_e_namaz": "date_of_fraez",
#             "wajibath_e_namaz": "date_of_wajibath",
#             "sana": "date_of_sana",
#             "sureh_fatihah": "date_of_sureh_fatihah",
#             "surah_e_feel": "date_of_surah_e_feel",
#             "surah_e_iqlas": "date_of_surah_e_iqlas",
#             "surah_e_falaq": "date_of_surah_e_falaq",
#             "surah_e_nas": "date_of_surah_e_nas",
#             "tasbihath_rukh_and_sajda": "date_of_tasbihath_rukh_and_sajda",
#             "attahiyath": "date_of_attahiyath",
#             "darood_e_ibrahim": "date_of_darood_e_ibrahim",
#             "duwa_e_masora": "date_of_duwa_e_masora",
#             "from_sana_to_salam": "date_of_sana_to_salam",
#             "sana_to_salam": "date_of_sana_to_salam_",
#             "duwa_balig_mard_ya_aurath": "date_of_duwa_balig_mard_ya_aurath",
#             "duwa_nabalig_bacha": "date_of_nabalig_bacha",
#             "duwa_nabalig_bachi": "date_of_nabalig_bachi",
#         }

#         # Loop through the field mappings and update the target document
#         for weekly_field, complete_field in field_mapping.items():
#             if student_progress.meta.has_field(complete_field):
#                 # Set the checkbox field
#                 weekly_value = doc.get(weekly_field)
#                 if weekly_value and not student_progress.get(complete_field):
#                     student_progress.set(complete_field, 1)  # Check the field

#                     # Handle date fields
#                     date_field = date_field_mapping.get(complete_field)  # Fetch from date mapping
#                     if date_field and student_progress.meta.has_field(date_field):
#                         # Populate date only if it was previously not set
#                         if not student_progress.get(date_field):
#                             student_progress.set(date_field, nowdate())

#         # Save the updated Student Complete Progress document
#         student_progress.save(ignore_permissions=True)
#         frappe.db.commit()

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Error updating Student Complete Progress")
        # frappe.throw(("An error occurred while updating the student's progress: ") + str(e))


# { groupName: "Group 1", fields: ["ghusol_farayez", "ghusol_sunath", "ghusol_nawaqis"] },
# { groupName: "Group 2", fields: ["wazu_farayez", "wazu_sunath", "wazu_nawaqis"] },
# { groupName: "Group 3", fields: ["sharayath_e_tayammum", "faraez_e_tayammum", "nawaqis_e_tayammum"] },
# { groupName: "Group 4", fields: ["fajar", "zohar", "asar","magrib","isha","juma"] },
# { groupName: "Group 5", fields: ["fraez_e_namaz", "wajibath_e_namaz", "sana","sureh_fatihah","surah_e_feel","surah_e_iqlas","surah_e_falaq","surah_e_nas","tasbihath_rukh_and_sajda","attahiyath","darood_e_ibrahim","duwa_e_masora","from_sana_to_salam"] },
# { groupName: "Group 6", fields: ["sana_to_salam"] },
# { groupName: "Group 6", fields: ["duwa_balig_mard_ya_aurath","duwa_nabalig_bacha","duwa_nabalig_bachi"] },


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



import frappe
from frappe.utils import nowdate

# Define the groups and their fields
field_groups = {
    "Group 1": ["ghusol_farayez", "ghusol_sunath", "ghusol_nawaqis"],
    "Group 2": ["wazu_farayez", "wazu_sunath", "wazu_nawaqis"],
    "Group 3": ["sharayath_e_tayammum", "faraez_e_tayammum", "nawaqis_e_tayammum"],
    "Group 4": ["fajar", "zohar", "asar", "magrib", "isha", "juma"],
    "Group 5": [
        "fraez_e_namaz", "wajibath_e_namaz", "sana", "sureh_fatihah", "surah_e_feel",
        "surah_e_iqlas", "surah_e_falaq", "surah_e_nas", "tasbihath_rukh_and_sajda",
        "attahiyath", "darood_e_ibrahim", "duwa_e_masora", "from_sana_to_salam"
    ],
    "Group 6": ["sana_to_salam"],
    "Group 7": ["duwa_balig_mard_ya_aurath", "duwa_nabalig_bacha", "duwa_nabalig_bachi"],
}

# Define the mapping of fields to their respective date fields
field_to_date_mapping = {
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

# Define the mapping of group names to display names
group_name_mapping = {
    "Group 1": "Ghusol (Bath)",
    "Group 2": "Wazu (Ablution)",
    "Group 3": "Tayammum",
    "Group 4": "Namaz",
    "Group 5": "Extended Namaz",
    "Group 6": "Practically Offer Two Rakath Namaz",
    "Group 7": "Namaz E Janaza"
}

@frappe.whitelist()
def fetch_progress(student_id, group_name):
    """
    Fetch progress data for a specific group for the given student.
    """
    if group_name not in field_groups:
        frappe.throw(f"Invalid group name: {group_name}")

    group_fields = field_groups[group_name]

    # Fetch or create the Student Complete Progress document
    student_progress = frappe.get_doc(
        "Student Complete Progress",
        {"student_name": student_id}
    ) if frappe.db.exists("Student Complete Progress", {"student_name": student_id}) else None

    if not student_progress:
        student_progress = frappe.get_doc({
            "doctype": "Student Complete Progress",
            "student_name": student_id,
        })
        student_progress.insert()
        frappe.db.commit()

    # Check progress
    unchecked_fields = []
    previously_checked_fields = {}
    for field in group_fields:
        checkbox_value = student_progress.get(field)
        if checkbox_value:
            previously_checked_fields[field] = 1
        else:
            unchecked_fields.append(field)

    # If all fields are checked, mark the group as completed
    is_group_complete = len(unchecked_fields) == 0

    # Get the display name for the group
    display_name = group_name_mapping.get(group_name, group_name)

    return {
        "status": "success",
        "unchecked_fields": unchecked_fields,
        "previously_checked_fields": previously_checked_fields,
        "is_group_complete": is_group_complete,
        "display_name": display_name,
    }


@frappe.whitelist()
def update_progress(student_id, selected_fields):
    """
    Update the Student Complete Progress doctype based on selected fields.
    """
    selected_fields = frappe.parse_json(selected_fields)

    # Fetch the Student Complete Progress document
    student_progress = frappe.get_doc("Student Complete Progress", {"student_name": student_id})

    # Update the fields in Student Complete Progress
    for field, is_checked in selected_fields.items():
        if is_checked:
            # Mark the field as checked
            student_progress.set(field, 1)

            # Get the corresponding date field from the mapping
            date_field = field_to_date_mapping.get(field)
            if date_field:
                student_progress.set(date_field, nowdate())

    # Save the document
    student_progress.save()
    frappe.db.commit()

    return {"status": "success", "message": "Progress updated successfully."}
