$('#discount-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: $(this).serialize(),

        success: function (data) {
            if (data.error) {
                console.log(data.error);
                   swal({
                            title: 'Error',
                            text: data.error,
                            type: 'warning',
                            icon: 'warning',
                        })
                $('input[name="code"]').val('');
            }
            if (data.total_price) {
                $('#final_price').html('Final Price: ' + data.total_price + ' $')
                $('#discount').remove()
            }

        },
        error: function (data) {

        }

    });

});
