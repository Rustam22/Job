/**
 * Created by rustam on 22.12.17.
 */

$(function() {

    $('#login-form-link').click(function(e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#register-form").fadeOut(100);
        $('#register-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#register-form-link').click(function(e) {
        $("#register-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });

    $('#register-form-link').click()
    $('#register-submit').click(function() {
        var  password_1 = $('#register-form #password').val().trim();
        var  password_2 = $('#register-form #confirm-password').val().trim();

        if(password_1 != password_2) {
            alert('Passwords are not matching');
            return false;
        }

    });
});