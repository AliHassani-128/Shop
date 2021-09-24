$("form").each(function () {

    $(this).bind("submit", function (event) {

        event.preventDefault();
        var formHTML = event.target;

        $.ajax({

            method: formHTML.method,
            url: formHTML.action,

            data: $(this).serialize(),
            success: function (result) {
                console.log(result.products);

                $('#product-count').html(result.products);
            }
            , error: function (error) {
                console.log(error.statusCode())
            }

        });

    });

});