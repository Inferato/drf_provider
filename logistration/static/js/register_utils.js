$(document).ready(function () {
    $('#id_username').blur(function () {
        checkUserExists();
    });

    $('#id_email').blur(function () {
        checkUserExists();
    });

    $('#id_password2').blur(function () {
        validatePassword();
    });

    $('#id_password1').blur(function () {
        validatePassword();
    });

    function checkUserExists() {
        var username = $('#id_username').val();
        var email = $('#id_email').val();
        var data = {'username': username}

        $.ajax({
            url: '/check_user_exists/',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function (data) {
                if (data.data.username_exists) {
                    $('#usernameError').text('This username is already taken.');
                } else {
                    $('#usernameError').text('');
                }
                
                if (data.data.email_exists) {
                    $('#emailError').text('This email is already registered.');
                } else {
                    $('#emailError').text('');
                    
                }
                if (data.user_check_errors) {
                    $('.demoClass').hide();
                    $('#registerButton').prop('disabled', true);
                } else {
                    $('.demoClass').show();
                    $('#registerButton').prop('disabled', false);
                    validatePassword();
                }
            }
        });
    }

    function validatePassword() {
        var password = $('#id_password1').val();
        var confirmPassword = $('#id_password2').val();
        var password_is_empty = password.length < 1
        if (!password_is_empty) {
            if (password !== confirmPassword) {
                $('#confirmPasswordError').text('Passwords do not match.');
                $('#registerButton').prop('disabled', true);
                $('.demoClass').hide()
            } else {
                $('#confirmPasswordError').text('');
                $('#registerButton').prop('disabled', false);
                $('.demoClass').show()
            }
        } else {
            $('#confirmPasswordError').text('Passwords can`t be empty.');
            $('#registerButton').prop('disabled', true);
            $('.demoClass').hide()
        }
        
    }
});