// frappe.ui.form.on('Student Learning Status', {
//     refresh: function (frm) {
//         frm.add_custom_button(__('Create Weekly Progress'), function () {
//             frappe.call({
//                 method: "shaheen_dev.api.custom_api.create_weekly_progress",
//                 args: {
//                     student_id: frm.doc.student_id
//                 },
//                 callback: function (response) {
//                     if (response.message && response.message.status === "success") {
//                         const uncheckedFields = response.message.unchecked_fields;
//                         const studentId = response.message.student_id;

//                         if (uncheckedFields.length > 0) {
//                             const dialog = new frappe.ui.Dialog({
//                                 title: 'Select Fields to Save',
//                                 fields: uncheckedFields.map(field => ({
//                                     label: field.replace(/_/g, ' '),
//                                     fieldname: field,
//                                     fieldtype: 'Check'
//                                 })),
//                                 primary_action_label: 'Save',
//                                 primary_action(values) {
//                                     frappe.call({
//                                         method: "frappe.client.insert",
//                                         args: {
//                                             doc: {
//                                                 doctype: "Weekly Student Progress",
//                                                 student_id: studentId,
//                                                 ...values
//                                             }
//                                         },
//                                         callback: function (saveResponse) {
//                                             if (saveResponse.message) {
//                                                 frappe.msgprint(__('Progress created successfully!'));
//                                                 dialog.hide();
//                                             }
//                                         },
//                                         error: function () {
//                                             frappe.msgprint(__('Failed to save progress.'));
//                                         }
//                                     });
//                                 }
//                             });

//                             dialog.show();
//                         } else {
//                             frappe.msgprint(__('No unchecked fields available for this student.'));
//                         }
//                     } else {
//                         frappe.msgprint(__('Failed to retrieve unchecked fields or an error occurred.'));
//                     }
//                 },
//                 error: function () {
//                     frappe.msgprint(__('Failed to call the server script.'));
//                 }
//             });
//         });
//     }
// });


// // frappe.ui.form.on('Student Learning Status', {
// //     refresh: function (frm) {
// //         frm.add_custom_button(__('Create Weekly Progress'), function () {
// //             frappe.msgprint(__('Custom button clicked!'));
// //         });
// //     }
// // });
