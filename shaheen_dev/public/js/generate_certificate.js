frappe.ui.form.on('Student Complete Progress', {
    generate_and_send_certificate: function(frm) {
        console.log('hiiiiiiiiiiiiiiiii')

                frappe.call({
                    method: "shaheen_dev.api.generate_certificate.generate_certificate",
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('Certificate generated successfully!'));
                            frm.reload_doc();
                        }
                    }
                });
         
        }
  
});
