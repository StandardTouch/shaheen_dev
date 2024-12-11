// $(document).ready(function () {
//     // Dynamically add Bootstrap Icons CDN if not already included
//     if (!$("link[href*='bootstrap-icons']").length) {
//         var link = document.createElement('link');
//         link.rel = 'stylesheet';
//         link.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css';
//         document.head.appendChild(link);
//     }

//     // Only display the navbar if we're on a desk page (not on login, signup, or reset-password)
//     if (frappe.get_route()[0] !== 'login' && frappe.get_route()[0] !== 'signup' && frappe.get_route()[0] !== 'reset-password') {

//         // Custom navbar HTML (the 3 buttons with href links)
//         var customNavbar = `
//             <div class="custom-navbar fixed-bottom d-flex justify-content-between p-3">
//                 <a href="/app/student-learning-status/Student Learning Status" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                    <i class="bi bi-search" style="font-size: 15px;"></i>
//                 </a>
//                 <a href="/app/molvi" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                     <i class="bi bi-house-door" style="font-size: 15px;"></i>
//                 </a>
//                 <a href="/app/query-report/Student Data with check field" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
//                     <i class="bi bi-clipboard-check"" style="font-size: 15px;"></i>
//                 </a>
//             </div>
//         `;
//         // Append the navbar to the bottom of the body
//         $('body').append(customNavbar);
//     }
// });
$(document).ready(function () {
    console.log("Custom Navbar Script Loaded");

    // Dynamically add Bootstrap Icons CDN if not already included
    if (!$("link[href*='bootstrap-icons']").length) {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css';
        document.head.appendChild(link);
    }

    // Only display the navbar if we're on a desk page (not on login, signup, or reset-password)
    // if (frappe.get_route()[0] !== 'login' && frappe.get_route()[0] !== 'signup' && frappe.get_route()[0] !== 'reset-password') {

    // Get the current user's roles
    var userRoles = frappe.user_roles;


    // Start building the custom navbar HTML
    var customNavbar = `
            <div class="custom-navbar fixed-bottom d-flex justify-content-between p-3">
                <a href="/app/student-learning-status/Student Learning Status" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
                    <i id="button" class="bi bi-search" style="font-size: 15px;"></i>
                </a>
        `;
    // Add the 'Home' button unless the user has the 'Molvi' role
    // if (userRoles.includes("Molvi") || userRoles.includes("Volunteer")) {
    //     customNavbar += `
    //         <a href="/app/student-registration/new-student-registration-xxsixahect" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
    //             <i class="bi bi-person-add" style="font-size: 15px;"></i>
    //         </a>
    //     `;
    // } else if (userRoles.includes("Admin @ Shaheen")) {
    //     customNavbar += `
    //         <a href="/app/namaz-e-registration" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
    //             <i class="bi bi-house-door" style="font-size: 15px;"></i>
    //         </a>
    // `;
    // }
    if (!userRoles.includes("Admin @ Shaheen")) {
        customNavbar += `
            <a href="/app/student-registration/new-student-registration-xxsixahect" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
                <i class="bi bi-person-add" style="font-size: 15px;"></i>
            </a>
        `;
    } else {
        customNavbar += `
            <a href="/app/namaz-e-registration" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
                <i class="bi bi-house-door" style="font-size: 15px;"></i>
            </a>
    `;
    }


    // Add the 'Query Report' button (you can also add conditions here if needed)
    // if (userRoles.includes("Admin @ Shaheen")) {
    //     customNavbar += `
    //             <a href="/app/query-report/Student Data with check field" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
    //                 <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
    //             </a>
    //         `;
    // } else {
    //     customNavbar += `
    //             <a href="/app/query-report/Report for molvi" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
    //                 <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
    //             </a>
    //         `;
    // }
    if (userRoles.includes("Admin @ Shaheen") || (userRoles.includes("Volunteer"))) {
        customNavbar += `
                <a href="/app/query-report/Student Data with check field" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
                    <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
                </a>
            `;
    } else {
        customNavbar += `
                <a href="/app/query-report/Report for molvi" class="btn btn-primary rounded-circle d-flex justify-content-center align-items-center" style="width: 40px; height: 40px;">
                    <i class="bi bi-clipboard-check" style="font-size: 15px;"></i>
                </a>
            `;
    }


    customNavbar += `</div>`;

    // Append the navbar to the bottom of the body
    $('body').append(customNavbar);
}
);
