// dashboard.js

// Function to toggle sub-menu visibility
function toggleSubMenu(menuId) {
  var subMenu = document.getElementById(menuId);
  if (subMenu.style.display === "block") {
    subMenu.style.display = "none";
  } else {
    subMenu.style.display = "block";
  }
}

// Function to handle user logout
function logoutUser() {
  var logoutUrl = document.getElementById('logout-btn').getAttribute('data-logout-url');
  window.location.href = logoutUrl;
}

// Initialize the bar chart
window.onload = function() {
  var ctx = document.getElementById('myBarChart').getContext('2d');
  var totalDrivers = document.getElementById('logout-btn').getAttribute('data-total-drivers');
  var totalVehicles = document.getElementById('logout-btn').getAttribute('data-total-vehicles');
  var totalCoDrivers = document.getElementById('logout-btn').getAttribute('data-total-codrivers');
  var totalProducts = document.getElementById('logout-btn').getAttribute('data-total-products');
  
  var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Drivers', 'Vehicles', 'Co-Drivers', 'Inventory'],
      datasets: [{
        label: '# of Entries',
        data: [totalDrivers, totalVehicles, totalCoDrivers, totalProducts],
        backgroundColor: [
          'rgba(54, 162, 235, 0.2)',  // Blue
          'rgba(75, 192, 192, 0.2)',  // Green
          'rgba(255, 159, 64, 0.2)',  // Orange
          'rgba(153, 102, 255, 0.2)'  // Purple
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',    // Blue
          'rgba(75, 192, 192, 1)',    // Green
          'rgba(255, 159, 64, 1)',    // Orange
          'rgba(153, 102, 255, 1)'    // Purple
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
};

// Function to bind event listeners to menu items
function initializeMenuToggle() {
  var menuItems = document.querySelectorAll('.nav-link[id$="-link"]');
  
  menuItems.forEach(function(menuItem) {
    menuItem.addEventListener('click', function(event) {
      event.preventDefault();
      var menuId = this.getAttribute('id').replace('-link', '-sub-menu');
      toggleSubMenu(menuId);
    });
  });
}

// Bind the logout function to the button click event
document.addEventListener("DOMContentLoaded", function() {
  var logoutBtn = document.getElementById('logout-btn');
  logoutBtn.addEventListener('click', logoutUser);
  
  // Initialize menu toggle functionality
  initializeMenuToggle();
});
