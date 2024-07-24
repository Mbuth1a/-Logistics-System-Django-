
        function goBackToDashboard() {
            // Replace with your dashboard URL
            window.location.href = "/dashboard";
        }

        document.getElementById('addCoDriverForm').addEventListener('submit', function(event) {
            var employeeNumber = document.getElementById('employeeNumber').value;
            var phoneNumber = document.getElementById('phoneNumber').value;
            var emailAddress = document.getElementById('emailAddress').value;

            // Check if phone number is exactly 10 digits
            if (phoneNumber.length !== 10) {
                alert('Phone number must be exactly 10 digits.');
                event.preventDefault(); // Prevent form submission
                return;
            }

            // Check if employee number starts with 'DCL'
            if (!employeeNumber.startsWith('DCL')) {
                alert('Employee number must start with "DCL".');
                event.preventDefault(); // Prevent form submission
                return;
            }

            // Check if email address ends with '@gmail.com'
            if (!emailAddress.endsWith('@gmail.com')) {
                alert('Email address must end with "@gmail.com".');
                event.preventDefault(); // Prevent form submission
                return;
            }
        });
   