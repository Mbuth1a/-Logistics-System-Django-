
        $(document).ready(function() {
            function loadVehicles() {
                $.ajax({
                    url: "{% url 'get_vehicles' %}",
                    method: "GET",
                    success: function(data) {
                        var vehicleTableBody = $('#vehicleTableBody');
                        vehicleTableBody.empty();
                        data.forEach(function(vehicle, index) {
                            vehicleTableBody.append(`
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${vehicle.vehicle_regno}</td>
                                    <td>${vehicle.vehicle_model}</td>
                                    <td>${vehicle.vehicle_type}</td>
                                    <td>${vehicle.engine_number}</td>
                                    <td>${vehicle.capacity}</td>
                                    <td>
                                        <button class="btn btn-orange btn-sm" onclick="editVehicle(${vehicle.id})"><i class="fas fa-edit"></i> Edit</button>
                                        <button class="btn btn-danger btn-sm" onclick="deleteVehicle(${vehicle.id})"><i class="fas fa-trash"></i> Delete</button>
                                    </td>
                                </tr>
                            `);
                        });
                    }
                });
            }

            loadVehicles();

            window.editVehicle = function(id) {
                $.ajax({
                    url: `/edit_vehicle/${id}/`,
                    method: "GET",
                    success: function(data) {
                        var vehicle = data;
                        $('#edit_vehicle_regno').val(vehicle.vehicle_regno);
                        $('#edit_vehicle_model').val(vehicle.vehicle_model);
                        $('#edit_vehicle_type').val(vehicle.vehicle_type);
                        $('#edit_engine_number').val(vehicle.engine_number);
                        $('#edit_capacity').val(vehicle.capacity);
                        $('#editVehicleModal').modal('show');

                        $('#editVehicleForm').off('submit').on('submit', function(e) {
                            e.preventDefault();
                            $.ajax({
                                url: `/edit_vehicle/${id}/`,
                                method: "POST",
                                data: $(this).serialize(),
                                success: function(response) {
                                    if (response.status === 'success') {
                                        $('#editVehicleModal').modal('hide');
                                        loadVehicles();
                                    } else {
                                        alert('Error updating vehicle.');
                                    }
                                }
                            });
                        });
                    }
                });
            };

            window.deleteVehicle = function(id) {
                $('#deleteVehicleModal').modal('show');

                $('#confirmDeleteButton').off('click').on('click', function() {
                    $.ajax({
                        url: `/delete_vehicle/${id}/`,
                        method: "POST",
                        data: {
                            csrfmiddlewaretoken: '{{ csrf_token }}'
                        },
                        success: function(response) {
                            if (response.status === 'success') {
                                $('#deleteVehicleModal').modal('hide');
                                loadVehicles();
                            } else {
                                alert('Error deleting vehicle.');
                            }
                        }
                    });
                });
            };

            window.viewVehicle = function(id) {
                // Implement view functionality if needed
                alert('View vehicle details feature is under construction.');
            };
        });
        function goToDashboard() {
            window.location.href = "{% url 'dashboard' %}";
        }
    