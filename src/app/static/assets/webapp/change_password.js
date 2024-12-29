$(document).ready(function(){
    $("#change_password_form").submit(function (event) {
        event.preventDefault();

        var data = new FormData(this);

        // Reset error messages
        const oldpasswordError = document.getElementById("oldpassword_error_div");
        const password1Error = document.getElementById("password1_error_div");
        const password2Error = document.getElementById("password2_error_div");

        oldpasswordError.innerHTML = '';
        password1Error.innerHTML = '';
        password2Error.innerHTML = '';

        const oldpassword = document.getElementById("id_oldpassword");
        const passwordInput = document.getElementById("id_password1");
        const confirmPasswordInput = document.getElementById("id_password2");

        const isPasswordValid = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,15}$/.test(passwordInput.value);

        let is_save = true;

        if (!oldpassword.value) {
            oldpasswordError.innerHTML = 'Enter Your Old password.';
            is_save = false;
        }

        if (!isPasswordValid) {
            password1Error.innerHTML = 'Password must be between 8 to 15 characters and contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character.';
            is_save = false;
        }

        if (!passwordInput.value) {
            password1Error.innerHTML = 'Enter Your New password.';
            is_save = false;
        }

        if (!confirmPasswordInput.value) {
            password2Error.innerHTML = 'Enter Your Confirm password.';
            is_save = false;
        }

        if (passwordInput.value !== confirmPasswordInput.value) {
            password2Error.innerHTML = 'Passwords do not match.';
            is_save = false;
        }

        if (is_save) {
            const url = "{% url 'users:change_password' %}";

            $.ajax({
                type: "POST",
                url: url,
                data: data,
                success: function (data) {
                    if (data.message_type === "error") {
                        $.toast({
                            text: data.message,
                            position: 'bottom-right',
                            stack: false,
                            icon: 'error',
                        });
                    } else {
                        $("#demo-modal").toggleClass("show-model");
                        $.toast({
                            text: "Password has been changed",
                            position: 'bottom-right',
                            stack: false,
                            icon: 'success',
                        });
                        setTimeout(function () {
                            window.location.reload(1);
                        }, 3000);
                    }
                },
                cache: false,
                contentType: false,
                processData: false
            });
        }
    });
})