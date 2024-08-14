document.addEventListener('DOMContentLoaded', function () {
    handleContactForm();
});

function handleContactForm() {
    const form = document.getElementById('contactForm');
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        console.log("Form Submitted");
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
            if(data.status==='success') {
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
