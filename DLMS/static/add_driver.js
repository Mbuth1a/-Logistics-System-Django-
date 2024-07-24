function goBackToDashboard() {
            // Replace with your dashboard URL
            window.location.href = "/dashboard";
        }

        // Function to move focus to the next input field on pressing Enter
        function moveFocus(current, nextInputId) {
            if (current.value.length === current.maxLength) {
                document.getElementById(nextInputId).focus();
            }
        }

        // Event listener to move focus to the next input field on Enter key press
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const focusableInputs = ['first_name', 'last_name', 'username', 'license_number', 'phone_number', 'email'];
                const currentInput = document.activeElement;
                const currentIndex = focusableInputs.indexOf(currentInput.id);
                if (currentIndex > -1 && currentIndex < focusableInputs.length - 1) {
                    e.preventDefault();
                    document.getElementById(focusableInputs[currentIndex + 1]).focus();
                }
            }
        });

        // Form submission validation
        document.getElementById('addDriverForm').addEventListener('submit', function(event) {
            var phoneNumber = document.getElementById('phone_number').value.trim();
            var email = document.getElementById('email').value.trim();

            // Check phone number format
            if (!/^\d{10}$/.test(phoneNumber)) {
                document.getElementById('phoneError').textContent = 'Phone number must be exactly 10 digits.';
                event.preventDefault(); // Prevent form submission
            } else {
                document.getElementById('phoneError').textContent = ''; // Clear error message
            }

            // Check email format
            if (!email.endsWith('@gmail.com')) {
                alert('Please enter an email with @gmail.com domain.');
                event.preventDefault(); // Prevent form submission
            }
        });
   