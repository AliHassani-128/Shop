$("form").each(function () {

    $(this).bind("submit", function (event) {

        event.preventDefault();
        var formHTML = event.target;

        $.ajax({

            method: formHTML.method,
            url: formHTML.action,

            data: $(this).serialize(),
            success: function (result) {
                console.log(result)
                console.log(typeof (result))
                var order = JSON.parse(result);
                $(`#price${order.id}`).html(order.price + ' $');
                $(`#quantity${order.id}`).html(order.quantity);
                $('#final_price').html('Final Price: ' + order.total_price + ' $')
            }
            , error: function (error) {
                console.log(error.statusCode())
            }

        });

    });

});