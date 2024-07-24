document.addEventListener('DOMContentLoaded', function() {
    fetchTrips();
});

function fetchTrips() {
    fetch('/api/trips/')
        .then(response => response.json())
        .then(trips => {
            displayTrips(trips);
        })
        .catch(error => {
            console.error('Error fetching trips:', error);
        });
}

function displayTrips(trips) {
    const tripTableBody = document.getElementById('trip-table-body');
    tripTableBody.innerHTML = '';

    trips.forEach(trip => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${trip.vehicle}</td>
            <td>${trip.day}</td>
            <td>${trip.date}</td>
            <td>${trip.time}</td>
            <td>${trip.description}</td>
            <td>${trip.from_location}</td>
            <td>${trip.to_location}</td>
            <td>${trip.driver}</td>
            <td>${trip.driver}</td>
            <td>${trip.co_driver}</td>
            
            <td>${trip.est_distance}</td>
            <td><button class="btn btn-primary btn-end-trip" onclick="EndTrip(${trip.id})">END-TRIP</button></td>
        `;
        tripTableBody.appendChild(tr);
    });
}

function EndTrip(tripId) {
    // Add functionality to view trip details
    window.location.href = `/trip/${tripId}/`;
}

function goToDashboard() {
    window.location.href = '/dtms_dashboard/';
}

function calculateTotalWeight() {
    const productSelect = document.getElementById('id_product');
    const quantityInput = document.getElementById('id_quantity');
    const totalWeightInput = document.getElementById('id_total_weight');
    
    const selectedProduct = productSelect.options[productSelect.selectedIndex];
    const weightPerMetre = parseFloat(selectedProduct.getAttribute('data-weight'));
    const quantity = parseFloat(quantityInput.value) || 0;
    
    const totalWeight = quantity * weightPerMetre;
    totalWeightInput.value = totalWeight.toFixed(2);
}


let originalOptions = [];

document.addEventListener('DOMContentLoaded', function() {
    // Store original options on page load
    const productSelect = document.getElementById('id_product');
    originalOptions = Array.from(productSelect.options);
});

function searchProduct() {
    const searchValue = document.getElementById('product_search').value.toLowerCase();
    const productSelect = document.getElementById('id_product');
    const options = productSelect.getElementsByTagName('option');
    
    let found = false;
    let firstMatchIndex = -1;
    
    // Reset options to their original state before filtering
    productSelect.innerHTML = '';
    originalOptions.forEach(option => productSelect.add(option));

    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        const stockCode = option.textContent.split(' - ')[0].toLowerCase();

        if (stockCode.includes(searchValue) && searchValue.trim() !== '') {
            option.style.display = '';
            if (firstMatchIndex === -1) {
                firstMatchIndex = i;  // Store index of the first match
            }
            found = true;
        } else {
            option.style.display = 'none';
        }
    }

    // Add placeholder if no options are visible
    if (!found) {
        productSelect.innerHTML = '<option value="" disabled selected>Search by product code</option>';
    } else {
        // Set the first matched product as selected
        if (firstMatchIndex !== -1) {
            productSelect.selectedIndex = firstMatchIndex;
        }
    }
}


function toggleQuantityInput() {
    const typeSelect = document.getElementById('id_type');
    const quantityLabel = document.querySelector('label[for="id_quantity"]');
    const quantityInput = document.getElementById('id_quantity');
    
    if (typeSelect.value === 'pieces') {
        quantityLabel.innerHTML = '<i class="fas fa-calculator"></i> Pieces';
        quantityInput.name = 'pieces';
    } else {
        quantityLabel.innerHTML = '<i class="fas fa-calculator"></i> Rolls';
        quantityInput.name = 'rolls';
    }
}
