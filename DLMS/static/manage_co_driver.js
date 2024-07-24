
        // Ensure jQuery is ready
        $(document).ready(function() {
    
            // Function to load co-drivers via AJAX
            function loadCoDrivers() {
                $.ajax({
                    url: "{% url 'get_codrivers' %}",
                    method: "GET",
                    success: function(data) {
                        var coDriverTableBody = $('#codriverTableBody');
                        coDriverTableBody.empty();
                        data.forEach(function(codriver, index) {
                            coDriverTableBody.append(`
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${codriver.employee_number}</td>
                                    <td>${codriver.co_driver_name}</td>
                                    <td>${codriver.phone_number}</td>
                                    <td>${codriver.email_address}</td>
                                    <td>
                                        <button class="btn btn-orange btn-sm" onclick="editCoDriver(${codriver.id})"><i class="fas fa-edit"></i> Edit</button>
                                        <button class="btn btn-danger btn-sm" onclick="deleteCoDriver(${codriver.id})"><i class="fas fa-trash"></i> Delete</button>
                                    </td>
                                </tr>
                            `);
                        });
                    }
                });
            }
    
            // Initial load of co-drivers
            loadCoDrivers();
    
            // Edit co-driver function
            window.editCoDriver = function(id) {
                $.ajax({
                    url: `/edit_codriver/${id}/`,
                    method: "GET",
                    success: function(data) {
                        var codriver = data;
                        $('#edit_employeeNumber').val(codriver.employee_number);
                        $('#edit_coDriverName').val(codriver.co_driver_name);
                        $('#edit_phoneNumber').val(codriver.phone_number);
                        $('#edit_emailAddress').val(codriver.email_address);
                        $('#editCoDriverModal').modal('show');
    
                        $('#editCoDriverForm').off('submit').on('submit', function(e) {
                            e.preventDefault();
                            $.ajax({
                                url: `/edit_codriver/${id}/`,
                                method: "POST",
                                data: $(this).serialize(),
                                success: function(response) {
                                    if (response.status === 'success') {
                                        $('#editCoDriverModal').modal('hide');
                                        loadCoDrivers();
                                    } else {
                                        alert('Error updating co-driver.');
                                    }
                                }
                            });
                        });
                    }
                });
            };
    
            // Delete co-driver function
            window.deleteCoDriver = function(id) {
                $('#deleteCoDriverModal').modal('show');
    
                $('#confirmDeleteCoDriverButton').off('click').on('click', function() {
                    $.ajax({
                        url: `/delete_codriver/${id}/`,
                        method: "POST",
                        success: function(response) {
                            if (response.status === 'success') {
                                $('#deleteCoDriverModal').modal('hide');
                                loadCoDrivers();
                            } else {
                                alert('Error deleting co-driver.');
                            }
                        }
                    });
                });
            };
        });
        function goToDashboard() {
            window.location.href = "{% url 'dashboard' %}";
        }
   