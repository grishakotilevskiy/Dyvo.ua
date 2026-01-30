document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Client side for speed only, server side also implemented
    const emailInput = document.getElementById('id_email');
    const passwordInput = document.getElementById('id_password');
    const confirmInput = document.getElementById('id_confirm_password');

    // Helper function to toggle error visibility
    function toggleError(element, errorId, condition) {
        const errorDiv = document.getElementById(errorId);
        if (condition) {
            // Error exists
            errorDiv.style.display = 'block';
            // Only add 'is-invalid' if the field isn't empty (don't punish empty fields immediately on load)
            if(element.value !== '') element.classList.add('is-invalid');
        } else {
            errorDiv.style.display = 'none';
            element.classList.remove('is-invalid');
        }
    }

    // Email validation function with regex
    function validateEmail() {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isInvalid = !re.test(emailInput.value) && emailInput.value !== '';

        const errorDiv = document.getElementById('emailError');
        if (isInvalid) {
            emailInput.classList.add('is-invalid');
            errorDiv.style.display = 'block';
        } else {
            emailInput.classList.remove('is-invalid');
            errorDiv.style.display = 'none';
        }
    }

    function validatePassword() {
        const val = passwordInput.value;
        const lenCheck = val.length >= 8;
        const hasLetters = /[a-zA-Z]/.test(val);
        const hasDigits = /[0-9]/.test(val);
        const latinCheck = hasLetters && hasDigits;

        document.getElementById('passwordErrorLength').style.display = lenCheck || val === '' ? 'none' : 'block';
        document.getElementById('passwordErrorLatin').style.display = (latinCheck || val === '') ? 'none' : 'block';

        if (lenCheck  && latinCheck) {
            passwordInput.classList.remove('is-invalid');
        } else if (val !== '') {
            passwordInput.classList.add('is-invalid');
        }
    }

    function validateConfirm() {
        const isMatch = confirmInput.value === passwordInput.value;
        const errorDiv = document.getElementById('confirmError');

        if (!isMatch && confirmInput.value !== '') {
            confirmInput.classList.add('is-invalid');
            errorDiv.style.display = 'block';
        } else {
            confirmInput.classList.remove('is-invalid');
            errorDiv.style.display = 'none';
        }
    }

    // Attach listeners
    if (emailInput) emailInput.addEventListener('blur', validateEmail);

    if (passwordInput) {
        passwordInput.addEventListener('blur', validatePassword);
        passwordInput.addEventListener('input', function() {
            if(confirmInput && confirmInput.value !== '') validateConfirm();
        });
    }

    if (confirmInput) confirmInput.addEventListener('blur', validateConfirm);


    // Searchable dropdown for region selection
    const regionInput = document.getElementById('regionInput');
    const regionWrapper = document.getElementById('regionWrapper');
    const regionList = document.getElementById('regionList');

    if (regionInput && regionWrapper && regionList) {
        const listItems = regionList.getElementsByTagName('li');

        regionInput.addEventListener('input', function() {
            const filter = regionInput.value.toLowerCase();
            regionWrapper.classList.add('active');

            for (let i = 0; i < listItems.length; i++) {
                const txtValue = listItems[i].textContent || listItems[i].innerText;
                if (txtValue.toLowerCase().startsWith(filter)) {
                    listItems[i].style.display = "";
                } else {
                    listItems[i].style.display = "none";
                }
            }

            if(filter === '') {
                for (let i = 0; i < listItems.length; i++) {
                    listItems[i].style.display = "";
                }
            }
        });

        regionInput.addEventListener('focus', function() {
            regionWrapper.classList.add('active');
            // Reset to show all on focus
            for (let i = 0; i < listItems.length; i++) {
                listItems[i].style.display = "";
            }
        });

        regionList.addEventListener('click', function(e) {
            if (e.target && e.target.nodeName === "LI") {
                regionInput.value = e.target.textContent;
                regionWrapper.classList.remove('active');
            }
        });

        document.addEventListener('click', function(e) {
            if (!regionWrapper.contains(e.target)) {
                regionWrapper.classList.remove('active');
            }
        });
    }
});
