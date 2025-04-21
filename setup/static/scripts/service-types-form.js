$(document).ready(function () {
    const userTypeField = $('#id_user_type');
    const serviceTypesField = $('#service-types-field');

    function toggleServiceTypes() {
        if (userTypeField.val() === 'provider') {
            serviceTypesField.show();
        } else {
            serviceTypesField.hide();
        }
    }

    // Executa ao carregar
    toggleServiceTypes();

    // Escuta mudanças
    userTypeField.on('change', toggleServiceTypes);
});