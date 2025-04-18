$(document).ready(function() {
    $('#address-input').on('input', function() {
        var query = $(this).val();
        if (query.length < 3) {
            $('#suggestions').empty();
            return;
        }

        $.ajax({
            url: 'https://nominatim.openstreetmap.org/search',
            data: {
                q: query,
                format: 'json',
                addressdetails: 1,
                limit: 8,
                countrycodes: 'BR'
            },
            success: function(data) {
                $('#suggestions').empty();
                data.forEach(function(item) {
                    $('#suggestions').append('<div class="autocomplete-suggestion" data-lat="' + item.lat + '" data-lon="' + item.lon + '">' + item.display_name + '</div>');
                });
            }
        });
    });

    $(document).on('click', '.autocomplete-suggestion', function() {
        var address = $(this).text();
        var lat = $(this).data('lat');
        var lon = $(this).data('lon');

        $('#address-input').val(address);
        $('#suggestions').empty();
      
    });
});