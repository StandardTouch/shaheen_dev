frappe.ui.form.on('Weekly Student Progress1', {
    refresh: function(frm) {
        frm.add_custom_button(('Generate Certificate'), function() {
            frappe.call({
                method: "shaheen_dev.api.generate_certificate.send_certificate",
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
