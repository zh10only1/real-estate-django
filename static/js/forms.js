document.addEventListener('DOMContentLoaded', function () {
    handleRegistrationFormCheckboxes()
    handleContactForm();
    handleRegistrationForm();
    handleOwnerForm();
});


function validateRadioWithTextInput(radioGroupName, otherRadioId, textInputId) {
    const otherRadio = document.getElementById(otherRadioId);
    const textInput = document.getElementById(textInputId);

    if (otherRadio.checked && textInput.value.trim() === '') {
        return false;
    }
    return true;
}

function validateHeatingSection() {
    return validateRadioWithTextInput('heating', 'heating_other', 'heating_specify');
}

function validatePropertyTypeSection() {
    return validateRadioWithTextInput('property_type', 'property_other', 'other_specify');
}

function handleOwnerForm() {
    const form = document.getElementById('owner-form');

    if (!form) {
        return;
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        if (!validateHeatingSection()) {
            alert('Please specify the heating system.');
            return;
        }

        if (!validatePropertyTypeSection()) {
            alert('Please specify the property type.');
            return;
        }

        const formData = new FormData(form);

        // Check file input for images
        const imageInput = document.getElementById('images');
        const files = imageInput.files;

        if (files.length > 0) {
            for (const file of files) {
                if (!['image/jpeg', 'image/png'].includes(file.type)) {
                    alert('Please upload only JPEG or PNG images.');
                    imageInput.value = ''; // Clear the file input
                    return;
                }
            }
        }

        // Prepare the form submission
        fetch('/send-owner-form/', {
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
                // alert('Ihre Anfrage wurde erfolgreich gesendet.');
                // Reset the form after successful submission
            } else {
                alert('Fehler beim Absenden des Formulars. Bitte versuchen Sie es später noch einmal.');
            }
            form.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            // alert('Ein Fehler ist aufgetreten. Bitte versuchen Sie es später noch einmal.');
        });
    });
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