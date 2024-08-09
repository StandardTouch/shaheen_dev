frappe.ui.form.on('Student Complete Progress', {
    refresh: function(frm) {
        // Add a custom button to the form view
        console.log('hiiiiiiiiiiiiiiiii')
        frm.add_custom_button(('Generate Certificate'), function() {
            frappe.call({
                method: "shaheen_dev.api.generate_certificate.generate_certificate",
                args: {
                    docname: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__('Certificate generated successfully!'));
                        frm.reload_doc();  // Reload the document to reflect any changes
                    }
                }
            });
        });
    }
});
