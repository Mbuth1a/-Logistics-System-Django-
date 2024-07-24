function goBackToDashboard() {
            // Replace with your dashboard URL
            window.location.href = "/dashboard";
        }
    
        document.getElementById('addVehicleForm').addEventListener('submit', function(event) {
            var vehicleRegNo = document.getElementById('id_vehicle_regno').value;
            var vehicleModel = document.getElementById('id_vehicle_model').value;
            var vehicleType = document.getElementById('id_vehicle_type').value;
            var engineNumber = document.getElementById('id_engine_number').value;
            var capacity = document.getElementById('id_capacity').value;

            if (!vehicleRegNo || !vehicleModel || !vehicleType || !engineNumber || !capacity) {
                alert('Please fill in all fields.');
                event.preventDefault(); // Prevent form submission
            }
        });
   