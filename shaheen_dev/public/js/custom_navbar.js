// // $(document).ready(function () {
// //     // Dynamically add Bootstrap Icons CDN if not already included
// //     if (!$("link[href*='bootstrap-icons']").length) {
// //         var link = document.createElement('link');
// //         link.rel = 'stylesheet';
// //         link.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css';
// //         document.head.appendChild(link);
// //     }

// //     // Only display the navbar if we're on a desk page (not on login, signup, or reset-password)
// //     if (frappe.get_route()[0] !== 'login' && frappe.get_route()[0] !== 'signup' && frappe.get_route()[0] !== 'reset-password') {

// //         // Custom navbar HTML (the 3 buttons with href links)
// //         var customNavbar = `
// //             <div class="custom-navbar fixed-bottom d-flex justify-content-between p-3">
// //                 <a href="/app/student-learning-status/Student Learning Status" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
// //                    <i class="bi bi-search" style="font-size: 15px;"></i>
// //                 </a>
// //                 <a href="/app/molvi" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
// //                     <i class="bi bi-house-door" style="font-size: 15px;"></i>
// //                 </a>
// //                 <a href="/app/query-report/Student Data with check field" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
// //                     <i class="bi bi-clipboard-check"" style="font-size: 15px;"></i>
// //                 </a>
// //             </div>
// //         `;
// //         // Append the navbar to the bottom of the body
// //         $('body').append(customNavbar);
// //     }
// // });
// $(document).ready(function () {
//     console.log("Custom Navbar Script Loaded");

//     // Dynamically add Bootstrap Icons CDN if not already included
//     if (!$("link[href*='bootstrap-icons']").length) {
//         var link = document.createElement('link');
//         link.rel = 'stylesheet';
//         link.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css';
//         document.head.appendChild(link);
//     }

//     // Only display the navbar if we're on a desk page (not on login, signup, or reset-password)
//     // if (frappe.get_route()[0] !== 'login' && frappe.get_route()[0] !== 'signup' && frappe.get_route()[0] !== 'reset-password') {

//     // Get the current user's roles
//     var userRoles = frappe.user_roles;


//     // Start building the custom navbar HTML
//     var customNavbar = `
//             <div class="custom-navbar fixed-bottom d-flex justify-content-between p-3">
//                 <a href="/app/student-learning-status/Student Learning Status" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                     <i id="button" class="bi bi-search" style="font-size: 15px;"></i>
//                 </a>
//         `;
//     // Add the 'Home' button unless the user has the 'Molvi' role
//     // if (userRoles.includes("Molvi") || userRoles.includes("Volunteer")) {
//     //     customNavbar += `
//     //         <a href="/app/student-registration/new-student-registration-xxsixahect" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//     //             <i class="bi bi-person-add" style="font-size: 15px;"></i>
//     //         </a>
//     //     `;
//     // } else if (userRoles.includes("Admin @ Shaheen")) {
//     //     customNavbar += `
//     //         <a href="/app/namaz-e-registration" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//     //             <i class="bi bi-house-door" style="font-size: 15px;"></i>
//     //         </a>
//     // `;
//     // }
//     if (!userRoles.includes("Admin @ Shaheen")) {
//         customNavbar += `
//             <a href="/app/student-registration/new-student-registration-xxsixahect" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-person-add" style="font-size: 15px;"></i>
//             </a>
//         `;
//     } else {
//         customNavbar += `
//             <a href="/app/namaz-e-registration" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-house-door" style="font-size: 15px;"></i>
//             </a>
//     `;
//     }


//     // Add the 'Query Report' button (you can also add conditions here if needed)
//     // if (userRoles.includes("Admin @ Shaheen")) {
//     //     customNavbar += `
//     //             <a href="/app/query-report/Student Data with check field" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//     //                 <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
//     //             </a>
//     //         `;
//     // } else {
//     //     customNavbar += `
//     //             <a href="/app/query-report/Report for molvi" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//     //                 <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
//     //             </a>
//     //         `;
//     // }
//     if (userRoles.includes("Admin @ Shaheen") || (userRoles.includes("Volunteer"))) {
//         customNavbar += `
//                 <a href="/app/query-report/Student Data with check field" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                     <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
//                 </a>
//             `;
//     } else {
//         customNavbar += `
//                 <a href="/app/query-report/Report for molvi" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                     <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
//                 </a>
//             `;
//     }


//     customNavbar += `</div>`;

//     // Append the navbar to the bottom of the body
//     $('body').append(customNavbar);
// }
// );


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




// $(document).ready(function () {
//     console.log("Custom Navbar Script Loaded");

//     // Dynamically add Bootstrap Icons CDN if not already included
//     if (!$("link[href*='bootstrap-icons']").length) {
//         var link = document.createElement('link');
//         link.rel = 'stylesheet';
//         link.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css';
//         document.head.appendChild(link);
//     }

//     // Get the current user's roles
//     var userRoles = frappe.user_roles;

//     // Start building the custom navbar HTML
//     var customNavbar = `
//         <div class="custom-navbar fixed-bottom d-flex justify-content-between p-3">
//             <a href="/app/student-learning-status/Student Learning Status" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-search" style="font-size: 15px;"></i>
//             </a>
//     `;

//     if (!userRoles.includes("Admin @ Shaheen")) {
//         customNavbar += `
//             <a href="/app/student-registration/new-student-registration-xxsixahect" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-person-add" style="font-size: 15px;"></i>
//             </a>
//         `;
//     } else {
//         customNavbar += `
//             <a href="/app/namaz-e-registration" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-house-door" style="font-size: 15px;"></i>
//             </a>
//         `;
//     }

//     if (userRoles.includes("Admin @ Shaheen") || userRoles.includes("Volunteer")) {
//         customNavbar += `
//             <a href="/app/query-report/Student Data with check field" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
//             </a>
//         `;
//     } else {
//         customNavbar += `
//             <a href="/app/query-report/Report for molvi" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
//             </a>
//         `;
//     }

//     // Add the new button to open the sidebar
//     customNavbar += `
//         <a href="#" id="openSidebarButton" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//             <i class="bi bi-list" style="font-size: 15px;"></i>
//         </a>
//     `;

//     customNavbar += `</div>`;

//     // Append the navbar to the bottom of the body
//     $('body').append(customNavbar);

//     // Sidebar HTML
//     var sidebar = `
//         <div id="customSidebar" class="custom-sidebar" style="position: fixed; right: -300px; top: 0; width: 300px; height: 100%; background: #f8f9fa; box-shadow: -2px 0 5px rgba(0,0,0,0.5); transition: right 0.3s; overflow-y: auto;">
//             <div class="p-3 border-bottom">
//                 <h5>User Details</h5>
//                 <button id="closeSidebarButton" class="btn btn-secondary btn-sm">Close</button>
//             </div>
//             <div class="p-3" id="sidebarContent">
//                 Loading user data...
//             </div>
//         </div>
//     `;
//     $('body').append(sidebar);

//     // Sidebar toggle logic
//     $('#openSidebarButton').click(function () {
//         $('#customSidebar').css('right', '0');
//         fetchUserData();
//     });

//     $('#closeSidebarButton').click(function () {
//         $('#customSidebar').css('right', '-300px');
//     });

//     // Function to fetch user data
//     function fetchUserData() {
//         var sidebarContent = $('#sidebarContent');
//         sidebarContent.html('Loading user data...');

//         // Fetch user data via API call
//         frappe.call({
//             method: "shaheen_dev.api.custom_api.get_assigned_masjid", // Replace with your actual app and module
//             callback: function (response) {
//                 if (response.message) {
//                     const { status, masjid, user_details, message } = response.message;

//                     if (status === "success") {
//                         sidebarContent.html(`
//                         <p><strong>Welcome:</strong> ${user_details.full_name}</p>
//                         <hr>
//                         <p><strong>Name:</strong> ${user_details.full_name}</p>
//                         <p><strong>Email:</strong> ${user_details.email}</p>
//                         <p><strong>Phone:</strong> ${user_details.phone || "Not Available"}</p>
//                         <p><strong>Assigned Masjid:</strong> ${masjid}</p>
//                     `);
//                     } else {
//                         sidebarContent.html(`
//                         <p><strong>Welcome:</strong> ${user_details.full_name}</p>
//                         <hr>
//                         <p><strong>Name:</strong> ${user_details.full_name}</p>
//                         <p><strong>Email:</strong> ${user_details.email}</p>
//                         <p><strong>Phone:</strong> ${user_details.phone || "Not Available"}</p>
//                         <p>${message}</p>
//                     `);
//                     }
//                 } else {
//                     sidebarContent.html('<p>Unable to load user data.</p>');
//                 }
//             },
//             error: function () {
//                 sidebarContent.html('<p>Error fetching user data. Please try again later.</p>');
//             }
//         });
//     }

// });



/////////////////////////////////////////////////////////////////////////////////////////////////




// $(document).ready(function () {
//     console.log("Custom Navbar Script Loaded");

//     // Dynamically add Bootstrap Icons CDN if not already included
//     if (!$("link[href*='bootstrap-icons']").length) {
//         var link = document.createElement('link');
//         link.rel = 'stylesheet';
//         link.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css';
//         document.head.appendChild(link);
//     }

//     // Get the current user's roles
//     var userRoles = frappe.user_roles;

//     // Start building the custom navbar HTML
//     var customNavbar = `
//         <div class="custom-navbar fixed-bottom d-flex justify-content-between p-3">
//             <a href="/app/student-learning-status/Student Learning Status" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-search" style="font-size: 15px;"></i>
//             </a>
//     `;

//     if (!userRoles.includes("Admin @ Shaheen")) {
//         customNavbar += `
//             <a href="/app/student-registration/new-student-registration-xxsixahect" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-person-add" style="font-size: 15px;"></i>
//             </a>
//         `;
//     } else {
//         customNavbar += `
//             <a href="/app/namaz-e-registration" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-house-door" style="font-size: 15px;"></i>
//             </a>
//         `;
//     }

//     if (userRoles.includes("Admin @ Shaheen") || userRoles.includes("Volunteer")) {
//         customNavbar += `
//             <a href="/app/query-report/Student Data with check field" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
//             </a>
//         `;
//     } else {
//         customNavbar += `
//             <a href="/app/query-report/Report for molvi" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                 <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
//             </a>
//         `;
//     }

//     // Add the new button to open the sidebar
//     customNavbar += `
//         <a href="#" id="openSidebarButton" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//             <i class="bi bi-list" style="font-size: 15px;"></i>
//         </a>
//     `;

//     customNavbar += `</div>`;

//     // Append the navbar to the bottom of the body
//     $('body').append(customNavbar);

//     // Sidebar HTML with new styling
//     var sidebar = `
//         <div id="customSidebar" class="custom-sidebar" style="position: fixed; right: -300px; top: 0; width: 300px; height: 100%; background: #f8f9fa; box-shadow: -2px 0 5px rgba(0,0,0,0.5); transition: right 0.3s; overflow-y: auto; padding: 20px;">
//             <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
//                 <h5 style="margin: 0; font-weight: bold;">User Details</h5>
//                 <button id="closeSidebarButton" class="btn btn-danger btn-sm" style="border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center;">
//                     <i class="bi bi-x" style="font-size: 20px;"></i>
//                 </button>
//             </div>
//             <hr>
//             <div id="sidebarContent" style="font-size: 14px; line-height: 1.8;">
//                 Loading user data...
//             </div>
//         </div>
//     `;
//     $('body').append(sidebar);

//     // Sidebar toggle logic
//     $('#openSidebarButton').click(function () {
//         $('#customSidebar').css('right', '0');
//         fetchUserData();
//     });

//     $('#closeSidebarButton').click(function () {
//         $('#customSidebar').css('right', '-300px');
//     });

//     // Function to fetch user data
//     function fetchUserData() {
//         var sidebarContent = $('#sidebarContent');
//         sidebarContent.html('Loading user data...');

//         // Fetch user data via API call
//         frappe.call({
//             method: "shaheen_dev.api.custom_api.get_assigned_masjid", // Corrected API path
//             callback: function (response) {
//                 if (response.message) {
//                     const { status, masjid, cluster_no, user_details, message } = response.message;

//                     if (status === "success") {
//                         sidebarContent.html(`
//                         <p><strong>Welcome:</strong> <span style="color: #007bff;">${user_details.full_name}</span></p>
//                         <hr>
//                         <p><strong>Name:</strong> ${user_details.full_name}</p>
//                         <p><strong>Email:</strong> ${user_details.email}</p>
//                         <p><strong>Phone:</strong> ${user_details.phone || "Not Available"}</p>
//                         <p><strong>Assigned Masjid:</strong> ${masjid}</p>
//                         <p><strong>Cluster No:</strong> ${cluster_no}</p>
//                     `);
//                     } else {
//                         sidebarContent.html(`
//                         <p><strong>Welcome:</strong> <span style="color: #007bff;">${user_details.full_name}</span></p>
//                         <hr>
//                         <p><strong>Name:</strong> ${user_details.full_name}</p>
//                         <p><strong>Email:</strong> ${user_details.email}</p>
//                         <p><strong>Phone:</strong> ${user_details.phone || "Not Available"}</p>
//                         <p>${message}</p>
//                     `);
//                     }
//                 } else {
//                     sidebarContent.html('<p>Unable to load user data.</p>');
//                 }
//             },
//             error: function () {
//                 sidebarContent.html('<p>Error fetching user data. Please try again later.</p>');
//             }
//         });
//     }

// });


////////////////////////////////////////////////////


$(document).ready(function () {
    console.log("Custom Navbar Script Loaded");

    // Dynamically add Bootstrap Icons CDN if not already included
    if (!$("link[href*='bootstrap-icons']").length) {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css';
        document.head.appendChild(link);
    }

    // Minimalistic Navbar with very light gray shade
    var customNavbar = `
        <div class="custom-navbar fixed-bottom d-flex justify-content-between p-3" style="background: #f0f0f0; border-top: 1px solid #cccccc;">
            <a href="/app/student-learning-status/Student Learning Status" class="btn btn-light rounded-circle d-flex justify-content-center align-items-center" style="width: 50px; height: 50px; background: #ffffff; color: #333333; border: 1px solid #cccccc;">
                <i class="bi bi-search" style="font-size: 20px;"></i>
            </a>
            <a href="/app/student-registration/new-student-registration-xxsixahect" class="btn btn-light rounded-circle d-flex justify-content-center align-items-center" style="width: 50px; height: 50px; background: #ffffff; color: #333333; border: 1px solid #cccccc;">
                <i class="bi bi-person-add" style="font-size: 20px;"></i>
            </a>
            <a href="/app/query-report/Student Data with check field" class="btn btn-light rounded-circle d-flex justify-content-center align-items-center" style="width: 50px; height: 50px; background: #ffffff; color: #333333; border: 1px solid #cccccc;">
                <i class="bi bi-clipboard-check" style="font-size: 20px;"></i>
            </a>
            <a href="#" id="openSidebarButton" class="btn btn-light rounded-circle d-flex justify-content-center align-items-center" style="width: 50px; height: 50px; background: #ffffff; color: #333333; border: 1px solid #cccccc;">
                <i class="bi bi-list" style="font-size: 20px;"></i>
            </a>
        </div>
    `;

    $('body').append(customNavbar);

    // Sidebar HTML
    var sidebar = `
        <div id="customSidebar" class="custom-sidebar" style="position: fixed; right: -300px; top: 0; width: 300px; height: 100%; background: #ffffff; box-shadow: -2px 0 10px rgba(0,0,0,0.1); transition: right 0.5s ease; overflow-y: auto; padding: 20px; border-left: 1px solid #cccccc;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <button id="closeSidebarButton" class="btn btn-light btn-sm" style="border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center; background: #f0f0f0; color: #333333; border: 1px solid #cccccc;">
                    <i class="bi bi-x" style="font-size: 20px;"></i>
                </button>
            </div>
            <div id="sidebarContent" style="font-size: 14px; line-height: 1.8; color: #333333; text-align: center;">
                <div id="userImageContainer" style="margin-bottom: 20px; text-align: center;">
                    <img src="https://i.imgur.com/1FoV8Xe.png" 
                        alt="Molvi Image" 
                        style="width: 100px; height: 100px; border-radius: 50%; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                </div>
                <p style="font-size: 18px; font-weight: bold; color: #333333;">Assalamu Alaikum, <span style="color: #333333;">Loading...</span></p>
            </div>
        </div>
    `;
    $('body').append(sidebar);

    // Sidebar toggle logic
    $('#openSidebarButton').click(function () {
        $('#customSidebar').css('right', '0');
        fetchUserData();
    });

    $('#closeSidebarButton').click(function () {
        $('#customSidebar').css('right', '-300px');
    });

    // Function to fetch user data
    function fetchUserData() {
        var sidebarContent = $('#sidebarContent');
        sidebarContent.html(`
            <div id="userImageContainer" style="margin-bottom: 20px; text-align: center;">
                <img src="https://i.imgur.com/1FoV8Xe.png" 
                    alt="Molvi Image" 
                    style="width: 100px; height: 100px; border-radius: 50%; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            </div>
            <p style="font-size: 18px; font-weight: bold; color: #333333;">Assalamu Alaikum, <span style="color: #333333;">Loading...</span></p>
        `);

        frappe.call({
            method: "shaheen_dev.api.custom_api.get_assigned_masjid",
            callback: function (response) {
                if (response.message) {
                    const { status, masjid, cluster_no, user_details, message } = response.message;

                    if (status === "success") {
                        sidebarContent.html(`
                            <p style="font-size: 18px; font-weight: bold; color: #333333; text-align: center;">
                                Assalamu Alaikum, <span style="color: #333333;">${user_details.full_name}</span>
                            </p>
                            <hr style="border: 1px solid #cccccc; margin: 20px 0;">
                            <div style="color: #333333; font-size: 14px; text-align: left;">
                                <p><strong>Name:</strong> ${user_details.full_name}</p>
                                <p><strong>Email:</strong> ${user_details.email}</p>
                                <p><strong>Phone:</strong> ${user_details.phone || "Not Available"}</p>
                                <p><strong>Assigned Masjid:</strong> ${masjid}</p>
                                <p><strong>Cluster No:</strong> ${cluster_no}</p>
                            </div>
                        `);
                    } else {
                        sidebarContent.html(`
                            <p style="font-size: 18px; font-weight: bold; color: #333333; text-align: center;">
                                Assalamu Alaikum, <span style="color: #333333;">${user_details.full_name}</span>
                            </p>
                            <hr style="border: 1px solid #cccccc; margin: 20px 0;">
                            <div style="color: #333333; font-size: 14px; text-align: left;">
                                <p><strong>Name:</strong> ${user_details.full_name}</p>
                                <p><strong>Email:</strong> ${user_details.email}</p>
                                <p><strong>Phone:</strong> ${user_details.phone || "Not Available"}</p>
                                <p>${message}</p>
                            </div>
                        `);
                    }
                } else {
                    sidebarContent.html('<p style="text-align: center; color: #333333;">Unable to load user data.</p>');
                }
            },
            error: function () {
                sidebarContent.html('<p style="text-align: center; color: #333333;">Error fetching user data. Please try again later.</p>');
            }
        });
    }
});
