frappe.listview_settings['File'] = {
    refresh: function(listview) {
        listview.page.add_actions_menu_item( ('Generate PDF from Folder Images'), function() {
            let selected_docs = listview.get_checked_items();

            if (selected_docs.length !== 1 || !selected_docs[0].is_folder) {
                frappe.msgprint(__('Please select exactly one folder.'));
                return;
            }

            let folder_name = selected_docs[0].name;
            let folder_path = selected_docs[0].folder ? `${selected_docs[0].folder}/${folder_name}` : folder_name;

            window.location.href = `/api/method/shaheen_dev.api.download_cert_pdf.generate_pdf_from_folder?folder_path=${folder_path}`;
        });
    }
};
