
        // $(document).ready(function() {
        //     function loadDrivers() {
        //         $.ajax({
        //             url: "{% url 'get_drivers' %}",
        //             method: "GET",
        //             success: function(data) {
        //                 var driverTableBody = $('#driverTableBody');
        //                 driverTableBody.empty();
        //                 data.forEach(function(driver, index) {
        //                     driverTableBody.append(`
        //                         <tr>
        //                             <td>${index + 1}</td>
        //                             <td>${driver.first_name}</td>
        //                             <td>${driver.last_name}</td>
        //                             <td>${driver.username}</td>
        //                             <td>${driver.license_number}</td>
        //                             <td>${driver.phone_number}</td>
        //                             <td>${driver.email}</td>
        //                             <td>
        //                                 <button class="btn btn-orange btn-sm" onclick="editDriver(${driver.id})"><i class="fas fa-edit"></i> Edit</button>
        //                                 <button class="btn btn-danger btn-sm" onclick="deleteDriver(${driver.id})"><i class="fas fa-trash"></i> Delete</button>
        //                             </td>
        //                         </tr>
        //                     `);
        //                 });
        //             }
        //         });
        //     }

        //     loadDrivers();

        //     window.editDriver = function(id) {
        //         $.ajax({
        //             url: `/edit_driver/${id}/`,
        //             method: "GET",
        //             success: function(data) {
        //                 var driver = data;
        //                 $('#edit_first_name').val(driver.first_name);
        //                 $('#edit_last_name').val(driver.last_name);
        //                 $('#edit_username').val(driver.username);
        //                 $('#edit_license_number').val(driver.license_number);
        //                 $('#edit_phone_number').val(driver.phone_number);
        //                 $('#edit_email').val(driver.email);
        //                 $('#editDriverModal').modal('show');

        //                 $('#editDriverForm').off('submit').on('submit', function(e) {
        //                     e.preventDefault();
        //                     $.ajax({
        //                         url: `/edit_driver/${id}/`,
        //                         method: "POST",
        //                         data: $(this).serialize(),
        //                         success: function(response) {
        //                             if (response.status === 'success') {
        //                                 $('#editDriverModal').modal('hide');
        //                                 loadDrivers();
        //                             } else {
        //                                 alert('Error updating driver.');
        //                             }
        //                         }
        //                     });
        //                 });
        //             }
        //         });
        //     };

        //     window.deleteDriver = function(id) {
        //         $('#deleteDriverModal').modal('show');

        //         $('#confirmDeleteDriverButton').off('click').on('click', function() {
        //             $.ajax({
        //                 url: `/delete_driver/${id}/`,
        //                 method: "POST",
        //                 success: function(response) {
        //                     if (response.status === 'success') {
        //                         $('#deleteDriverModal').modal('hide');
        //                         loadDrivers();
        //                     } else {
        //                         alert('Error deleting driver.');
        //                     }
        //                 }
        //             });
        //         });
        //     };
        // });
        // function goToDashboard() {
        //     window.location.href = "{% url 'dashboard' %}";
        // }
    