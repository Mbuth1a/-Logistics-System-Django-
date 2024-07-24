
    document.addEventListener('DOMContentLoaded', function() {
      // Fetch and display the initial list of products
      fetchProducts();

      // Handle form submission
      document.getElementById('addProductForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const form = this;
        const formData = new FormData(form);

        fetch(form.action, {
          method: 'POST',
          headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
          },
          body: formData,
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            addProductToTable(data.product);
            form.reset();
            $('#addProductModal').modal('hide');
          } else {
            alert('Error adding product');
          }
        })
        .catch(error => console.error('Error:', error));
      });

      // Handle search
      document.getElementById('searchButton').addEventListener('click', function() {
        searchProducts();
      });

      // Enable search on Enter key press
      document.getElementById('search-bar').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
          searchProducts();
        }
      });
    });

    function fetchProducts() {
      fetch('{% url "get_products" %}')
        .then(response => response.json())
        .then(data => {
          const productTableBody = document.getElementById('productTable').getElementsByTagName('tbody')[0];
          productTableBody.innerHTML = '';
          data.products.forEach(product => {
            addProductToTable(product);
          });
        })
        .catch(error => console.error('Error:', error));
    }

    function addProductToTable(product) {
      const productTableBody = document.getElementById('productTable').getElementsByTagName('tbody')[0];
      const newRow = productTableBody.insertRow();
      const count = productTableBody.getElementsByTagName('tr').length;

      newRow.innerHTML = `
        <td>${count}</td>
        <td>${product.description}</td>
        <td>${product.stock_code}</td>
        <td>${product.product}</td>
        <td>${product.unit_of_measure}</td>
        <td>${product.weight_per_metre}</td>
      `;
    }

    function searchProducts() {
      const filter = document.getElementById('search-bar').value.toUpperCase();
      const rows = document.getElementById('productTable').getElementsByTagName('tbody')[0].getElementsByTagName('tr');
      Array.from(rows).forEach(function(row) {
        const stockCode = row.cells[2].textContent || row.cells[2].innerText;
        if (stockCode.toUpperCase().indexOf(filter) > -1) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    }
    function goToDashboard() {
      window.location.href = "{% url 'dashboard' %}";
  }
