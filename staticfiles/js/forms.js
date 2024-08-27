let captcha_user_input = document.getElementById("captcha_user_input");
let captcha_text = ""

window.addEventListener("load", () => {
    let captcha_reload_btn = document.getElementById("captcha_reload_btn")
    captcha_reload_btn.addEventListener("click", () => reloadCaptcha())
    reloadCaptcha()
});

// Generate text
function textGenerator() {
    let generatedText = "";

    // String.fromcharcode gives ASCII values from given number, total 9 letters hence loop of 3
    for (let i = 0; i < 3; i++) {
        // 65-90 numbers are capital letters
        generatedText += String.fromCharCode(randomNumber(65, 90))
        // 97-122 are small letters
        generatedText += String.fromCharCode(randomNumber(97, 122))
        // 48-57 are numbers
        generatedText += String.fromCharCode(randomNumber(48, 57))
    }
    return generatedText
}

// Generating random numbers
function randomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min)
}

// Drawing text on canvas
function drawTextOnCanvas(text) {
    let canvas = document.getElementById("canvas");
    let ctx = canvas.getContext("2d")

    // clear canvas
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)

    // array of text color
    const textColor = ["rgba(0,0,0,0.8)", "rgba(71, 45, 255, 1)"]

    // space b/w lettes
    const letterSpace = 150 / text.length

    // loop through string
    for (let i = 0; i < text.length; i++) {
        // definding initial space for x axis
        const xInitialSpace = 25
        ctx.font = "20px Roboto Mono"
        // set text color
        ctx.fillStyle = textColor[randomNumber(0, 1)]
        ctx.fillText(text[i], xInitialSpace + i * letterSpace, randomNumber(25, 40), 100)
    }
}

// initial function
function reloadCaptcha() {
    // clearing input
    captcha_user_input.value = ""
    captcha_text = textGenerator()
    // randomize the text so that everytime the position of numbers and small letters is random
    captcha_text = [...captcha_text].sort(() => Math.random() - 0.5).join("")
    drawTextOnCanvas(captcha_text)
}

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

        if (captcha_user_input.value !== captcha_text) {
            alert("Invalid captcha. Please try again.")
            reloadCaptcha();
            return;
        };

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

        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
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
                if (submitButton) {
                    submitButton.disabled = false;
                }
                reloadCaptcha();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again later.');
                if (submitButton) {
                    submitButton.disabled = false;
                }
                reloadCaptcha();
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

        if (captcha_user_input.value !== captcha_text) {
            alert("Invalid captcha. Please try again.")
            reloadCaptcha();
            return;
        };

        changeCheckboxValue()
        const fileInput = document.getElementById('business_license');
        const file = fileInput.files[0];

        if (file && file.type !== 'application/pdf') {
            alert('Please upload a PDF file for Gewerbeanmeldung.');
            fileInput.value = ''; // Clear the file input
            return;
        }

        const submitButton = form.querySelector('button[type="submit"]');
        console.log(submitButton)
        if (submitButton) {
            submitButton.disabled = true;
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
                if (submitButton) {
                    submitButton.disabled = false;
                }
                reloadCaptcha();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again later.');
                if (submitButton) {
                    submitButton.disabled = false;
                }
                reloadCaptcha();
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

        if (captcha_user_input.value !== captcha_text) {
            alert("Invalid captcha. Please try again.")
            reloadCaptcha();
            return;
        };

        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
        }

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
                if (submitButton) {
                    submitButton.disabled = false;
                }
                reloadCaptcha();
            })
            .catch(error => {
                console.error('Cannot parse the content to json:', error);
                alert('An error occurred. Please try again later.');
                if (submitButton) {
                    submitButton.disabled = false;
                }
                reloadCaptcha();
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