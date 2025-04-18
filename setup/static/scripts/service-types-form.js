$(document).ready(function() {
    $('#id_user_type').change(function() {
        if ($(this).val() === 'provider') {
            $('#service-types-field').show();
        } else {
            $('#service-types-field').hide();
        }
    });
});