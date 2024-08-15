document.addEventListener('DOMContentLoaded', function () {
    handleContactForm();
    handleRegistrationForm();
});

function handleRegistrationForm() {
    const form = document.getElementById('registrationForm');
    const fileInput = document.getElementById('business_license');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const file = fileInput.files[0];

        if (file && file.type !== 'application/pdf') {
            alert('Please upload a PDF file for Gewerbeanmeldung.');
            fileInput.value = ''; // Clear the file input
            return;
        }

        const formData = new FormData(form);
        fetch('/send-registration-email/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Form submitted successfully!');
                form.reset(); // Clear the form fields
            } else {
                alert('Error submitting form: ' + data.message);
                form.reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });

    });
}

function handleContactForm() {
    const form = document.getElementById('contactForm');
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Send the data to Django via AJAX
        fetch('/send-email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Email sent successfully');
                }
                else {
                    console.error('Error sending email:', data.message);
                }
                form.reset();
            })
            .catch(error => {
                console.error('Cannot parse the content to json:', error);
            });
    });
}
