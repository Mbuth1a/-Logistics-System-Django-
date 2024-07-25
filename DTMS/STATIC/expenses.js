$(document).ready(function() {
    fetchTrips();
    
    function fetchTrips() {
        $.ajax({
            url: "{% url 'fetch_trips' %}",
            method: 'GET',
            success: function(response) {
                let tripsList = $('#tripsList');
                tripsList.empty();
                response.forEach(function(trip) {
                    let tableRow = `<tr data-id="${trip.id}">
                                    <td>${trip.id}</td>
                                    <td>${trip.vehicle}</td>
                                    <td>${trip.date}</td>
                                    <td>${trip.from_location}</td>
                                    <td>${trip.to_location}</td>
                                    <td>${trip.driver}</td>
                                    <td>${trip.co_driver}</td>
                                    <td><button class="btn btn-primary" onclick="openModal(${trip.id})">Assign Expense</button></td>
                                </tr>`;
                    tripsList.append(tableRow);
                });
                fetchAssignedExpenses(); // Fetch assigned expenses on load
            },
            error: function(error) {
                console.error('Error fetching trips:', error);
            }
        });
    }
    
    window.openModal = function(tripId) {
        $.ajax({
            url: "{% url 'get_trip_details' %}",
            method: 'GET',
            data: { trip_id: tripId },
            success: function(trip) {
                $('#tripId').val(trip.id);
                $('#regNo').val(trip.vehicle); // Ensure vehicle registration number is correctly passed
                $('#driverName').val(trip.driver.full_name);
                $('#coDriverName').val(trip.co_driver.co_driver_name);
                $('#driverExpense').val('');
                $('#coDriverExpense').val('');
                $('#tripDate').val(trip.date);
                $('#fromLocation').val(trip.from_location);
                $('#toLocation').val(trip.to_location);
                $('#expenseModal').modal('show');
            },
            error: function(error) {
                console.error('Error fetching trip details:', error);
            }
        });
    }
    
    window.saveExpenses = function() {
        let tripId = $('#tripId').val();
        let driverExpense = $('#driverExpense').val();
        let coDriverExpense = $('#coDriverExpense').val();
        
        $.ajax({
            url: "{% url 'assign_expenses' %}",
            method: 'POST',
            data: {
                trip_id: tripId,
                driver_expense: driverExpense,
                co_driver_expense: coDriverExpense,
                csrfmiddlewaretoken: '{{ csrf_token }}'  // Ensure CSRF token is included
            },
            success: function(response) {
                $('#expenseModal').modal('hide');
                fetchTrips();
            },
            error: function(error) {
                console.error('Error assigning expenses:', error);
            }
        });
    }

    function fetchAssignedExpenses() {
        $.ajax({
            url: "{% url 'fetch_assigned_expenses' %}",
            method: 'GET',
            success: function(response) {
                let expensesList = $('#expensesList');
                expensesList.empty();
                response.forEach(function(expense) {
                    let tableRow = `<tr>
                                    <td>${expense.trip_id}</td>
                                    <td>${expense.vehicle}</td>
                                    <td>${expense.date}</td>
                                    <td>${expense.from_location}</td>
                                    <td>${expense.to_location}</td>
                                    <td>${expense.driver_name}</td>
                                    <td>${expense.co_driver_name}</td>
                                    <td>${expense.driver_expense}</td>
                                    <td>${expense.co_driver_expense}</td>
                                </tr>`;
                    expensesList.append(tableRow);
                });
            },
            error: function(error) {
                console.error('Error fetching assigned expenses:', error);
            }
        });
    }

    window.toggleDoneExpenses = function() {
        $('#doneExpensesList').toggle();
    }

    window.goBackToDashboard = function() {
        window.location.href = "{% url 'dtms_dashboard' %}";
    }
});