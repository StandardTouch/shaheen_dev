import frappe

def redirect_user():
    user = frappe.session.user
    # Check the role of the user
    if "Molvi" in frappe.get_roles(user):
        # Redirect to a specific page if the user has a specific role
        frappe.local.response["home_page"] = "/app/student-learning-status/Student Learning Status"
