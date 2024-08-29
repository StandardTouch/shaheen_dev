frappe.ui.form.on('Weekly Student Progress', {
    before_submit: function(frm) {
        const fieldsToCheck = [
            'farayez_ghusol',
            'sunath_ghusol',
            'nawaqis_ghusol',
            'farayez',
            'sunath',
            'nawaqis',
            'fraez_e_namaz',
            'wajibath_e_namaz',
            'sana',
            'sureh_fatihah',
            'zammi_surah',
            'tasbihath_rukh_and_sajda',
            'attahiyath',
            'darood_e_ibrahim',
            'duwa_e_masora',
            'from_sana_to_salam',
            'nafeel_namaz',
            'namaz_e_janaza'
        ];
    
        // Function to check if all fields are checked
        function areAllFieldsChecked() {
            for (let i = 0; i < fieldsToCheck.length; i++) {
                console.log(fieldsToCheck[i])
                if (frm.doc[fieldsToCheck[i]] === 0){
                    console.log('\n\n\n\n\n\n\n\n\n\n\n\n')
                    console.log(fieldsToCheck[i])
                    return false;
                }
            }
            return true;
        }
    
        // Check if all fields are checked before generating the certificate
        if (areAllFieldsChecked()) {
            console.log('Generating certificate');

            frappe.call({
                method: "shaheen_dev.api.generate_certificate.generate_send_certificate",
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
        } 
    }
});
