document.addEventListener('DOMContentLoaded', function () {
    handleRegistrationFormCheckboxes()
    handleContactForm();
    handleRegistrationForm();
});

function handleRegistrationFormCheckboxes() {
    const realtorCheckbox = document.getElementById('realtor');
    const constructionCheckbox = document.getElementById('construction');

    if (!realtorCheckbox || !constructionCheckbox) {
        return;
    }

    // Function to handle checkbox change
    realtorCheckbox.addEventListener('change', function () {
        if (this.checked) {
            constructionCheckbox.checked = false; // Uncheck the other checkbox
        }
    });

    constructionCheckbox.addEventListener('change', function () {
        if (this.checked) {
            realtorCheckbox.checked = false; // Uncheck the other checkbox
        }
    });
}

function isOneCheckboxChecked() {
    const realtorCheckbox = document.getElementById('realtor');
    const constructionCheckbox = document.getElementById('construction');

    if (!realtorCheckbox || !constructionCheckbox) {
        return false;
    }
    return realtorCheckbox.checked || constructionCheckbox.checked;
}

function changeCheckboxValue() {
    const realtorCheckbox = document.getElementById('realtor');
    const constructionCheckbox = document.getElementById('construction');

    if (realtorCheckbox.checked) {
        realtorCheckbox.value = 'true';
        constructionCheckbox.value = 'false'; // Set unchecked checkbox to 'false'
    } else if (constructionCheckbox.checked) {
        constructionCheckbox.value = 'true';
        realtorCheckbox.value = 'false'; // Set unchecked checkbox to 'false'
    }
}

function handleRegistrationForm() {
    const form = document.getElementById('registrationForm');

    if (!form) {
        return;
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        if (!isOneCheckboxChecked()) {
            alert('Please select one of the checkboxes (Immobilienmakler or Bauunternehmen).');
            return;
        }

        changeCheckboxValue()
        const fileInput = document.getElementById('business_license');
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
                    console.log('Form submitted successfully!');
                } else {
                    alert('Error submitting form. Please try again later.');
                }
                form.reset();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again later.');
            });
    });
}

function handleContactForm() {
    const form = document.getElementById('contactForm');

    if (!form) {
        return;
    }

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
                    console.log('Form submitted successfully');
                }
                else {
                    alert('Error submitting form. Please try again later.');
                }
                form.reset();
            })
            .catch(error => {
                console.error('Cannot parse the content to json:', error);
            });
    });
}
