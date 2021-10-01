$('#discount-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: $(this).serialize(),
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
        },
        success: function (data) {
            $('#final_price').html('Final Price: ' + data.total_price + ' $')
            $('#discount').remove()

        },
        error: function () {
            console.log('error');
        }

    });

});
