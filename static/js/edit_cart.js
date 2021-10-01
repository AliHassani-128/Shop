$("form").each(function () {

    $(this).bind("submit", function (event) {
        var formHTML = event.target;
        if(formHTML.method === 'get'){
            event.preventDefault();
            $.ajax({

                method: formHTML.method,
                url: formHTML.action,

                data: $(this).serialize(),
                success: function (result) {
                    var order = JSON.parse(result);
                    if (order.delete){
                        $(`#order${order.id}`).remove();
                        var count = parseInt($('#product-count').html());
                        if(count != 1){
                            count -= 1 ;
                            $('#product-count').html(count.toString())
                        }
                        else{
                            $('#product-count').html('0')
                        }
                        $('#final_price').html('Final Price: ' + order.total_price + ' $')

                    }
                    else {
                        $(`#price${order.id}`).html(order.price + ' $');
                        $(`#quantity${order.id}`).html(order.quantity);
                        $('#final_price').html('Final Price: ' + order.total_price + ' $')
                    }

                    }
                , error: function (error) {
                    console.log(error.statusCode())
                }

            });}



    });

});