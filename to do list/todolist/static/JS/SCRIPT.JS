document.addEventListener('DOMContentLoaded', function () {
    const taskForm = document.getElementById('task-form');
    const errorMessageDiv = document.getElementById('error-message');

    taskForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(taskForm);

        fetch(taskForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Indicate that this is an AJAX request
                'X-CSRFToken': getCookie('csrftoken') // Send the CSRF token
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // Show the error message
                errorMessageDiv.textContent = data.error;
                errorMessageDiv.style.display = 'block'; // Show the error message div
            } else if (data.success) {
                // Optionally reset the form or update the page in some way
                taskForm.reset();
                errorMessageDiv.style.display = 'none'; // Hide the error message
                // You can also add a success message here if needed
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessageDiv.textContent = "An unexpected error occurred.";
            errorMessageDiv.style.display = 'block'; // Show the error message div
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Check if this cookie string begins with the name we want
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
