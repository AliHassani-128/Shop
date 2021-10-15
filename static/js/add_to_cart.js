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

                    $('#product-count').html(result.products);

                }
                , error: function (error) {
                    console.log(error.statusCode())
                }

            });

        }
    });


});