$("form").each(function () {
    $(this).bind("submit", function (event) {

        var formHTML = event.target;
        if (formHTML.method === 'get') {
            event.preventDefault();
            $.ajax({

                method: formHTML.method,
                url: formHTML.action,

                data: $(this).serialize(),
                success: function (result) {
                    var order = JSON.parse(result);
                    console.log(order.id)
                    $(`#order${order.id}`).remove();
                    $('#final_price').html('Final Price: ' + order.total_price + ' $')

                }
                , error: function (error) {
                    console.log(error.statusCode())
                }

            });

        }
    });


});