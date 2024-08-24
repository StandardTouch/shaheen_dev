frappe.ui.form.on('Add Demo', {
    refresh: function(frm) {
        frm.add_custom_button(__('Send WhatsApp Video to'), function() {
            frappe.call({
                method: 'shaheen_dev.api.whatsapp_video_api.send_whatsapp_with_video',
                args: {
                    docname: frm.doc.name
                },
                callback: function(response) {
                    console.log(response)
                    frappe.msgprint(__('WhatsApp video sending initiated.'));
                }
            });
        });
    }
});
