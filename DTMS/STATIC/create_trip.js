
        // Function to convert coordinates to address (reverse geocoding)
        function reverseGeocodeCoordinates(lat, lng, callback) {
            var url = "https://map-geocoding.p.rapidapi.com/json";
            var querystring = { "latlng": lat + "," + lng };
            var headers = {
                "x-rapidapi-key": "41d3ce4b7dmshd1e6bb368411d09p1f7b9cjsn3dba453520cf",
                "x-rapidapi-host": "map-geocoding.p.rapidapi.com"
            };
    
            $.ajax({
                url: url,
                type: 'GET',
                headers: headers,
                data: querystring,
                success: function(response) {
                    if (response.results && response.results[0]) {
                        callback(response.results[0].formatted_address);
                    } else {
                        alert('Unable to reverse geocode coordinates.');
                    }
                },
                error: function(err) {
                    console.error('Error in reverse geocoding:', err);
                    alert('Error reverse geocoding coordinates. Please try again later.');
                }
            });
        }
    
        // Function to convert address to coordinates (geocoding)
        function geocodeAddress(address, callback) {
            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({ 'address': address }, function (results, status) {
                if (status === 'OK') {
                    var location = results[0].geometry.location;
                    callback(location.lat(), location.lng());
                } else {
                    alert('Geocode was not successful for the following reason: ' + status);
                }
            });
        }
    
        // Function to calculate distance using RapidAPI Distance Matrix API
        function calculateDistance() {
            var origin = document.getElementById('id_from_location').value.trim();
            var destination = document.getElementById('id_to_location').value.trim();
    
            if (!origin || !destination) {
                alert('Please enter both locations.');
                return;
            }
    
            // Convert addresses to coordinates
            geocodeAddress(origin, function (originLat, originLng) {
                geocodeAddress(destination, function (destinationLat, destinationLng) {
                    var payload = {
                        "g": [
                            [originLng, originLat],
                            [destinationLng, destinationLat]
                        ],
                        "a": ["distance", "duration"]
                    };
    
                    var headers = {
                        "x-rapidapi-key": "41d3ce4b7dmshd1e6bb368411d09p1f7b9cjsn3dba453520cf",
                        "x-rapidapi-host": "distance-matrix-api-california.p.rapidapi.com",
                        "Content-Type": "application/json"
                    };
    
                    $.ajax({
                        url: "https://distance-matrix-api-california.p.rapidapi.com/us/california",
                        type: 'POST',
                        headers: headers,
                        data: JSON.stringify(payload),
                        success: function (response) {
                            var estimatedDistance = response.distance; // Adjust according to API response structure
                            document.getElementById('id_est_distance').value = estimatedDistance;
                        },
                        error: function (err) {
                            console.error('Error fetching distance:', err);
                            alert('Error calculating distance. Please try again later.');
                        }
                    });
                });
            });
        }
    
        // Function to move focus to the next input field on pressing Enter
        function moveFocus(current, nextInputId) {
            if (current.value.length === current.maxLength) {
                document.getElementById(nextInputId).focus();
            }
        }
    
        // Event listener to move focus to the next input field on Enter key press
        document.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                const focusableInputs = ['id_date', 'id_time', 'id_day', 'id_description', 'id_driver', 'id_co_driver', 'id_vehicle', 'id_from_location', 'id_to_location', 'id_est_distance'];
                const currentInput = document.activeElement;
                const currentIndex = focusableInputs.indexOf(currentInput.id);
                if (currentIndex > -1 && currentIndex < focusableInputs.length - 1) {
                    e.preventDefault();
                    document.getElementById(focusableInputs[currentIndex + 1]).focus();
                }
            }
        });
    
        // Form submission validation
        document.getElementById('createTripForm').addEventListener('submit', function (event) {
            var fromLocation = document.getElementById('id_from_location').value.trim();
            var toLocation = document.getElementById('id_to_location').value.trim();
    
            if (fromLocation === "" || toLocation === "") {
                alert('Please fill in all required fields.');
                event.preventDefault(); // Prevent form submission
            }
        });
    
        // Function to set the current day in the day input field based on the date input
        function setDayFromDate() {
            var dateInput = document.getElementById('id_date').value;
            if (dateInput) {
                var date = new Date(dateInput);
                var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                var day = days[date.getDay()];
                document.getElementById('id_day').value = day;
            } else {
                document.getElementById('id_day').value = '';
            }
        }
    
        // Add event listener to the date input field
        document.getElementById('id_date').addEventListener('change', setDayFromDate);
    
        // Set the current day on page load if date is pre-filled
        window.onload = function () {
            setDayFromDate();
        };
    
        function goToDashboard() {
            window.location.href = "{% url 'dtms_dashboard' %}";
        }
    