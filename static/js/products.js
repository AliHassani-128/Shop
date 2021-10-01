var url = 'http://127.0.0.1:8000/api/v1/products/?page=1';
$(document).ready(function () {
    load_page(url);
})

function load_page(url) {
    $(document).ready(function () {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                console.log(response)
                $('#row').html('');
                for (var product of response.results) {
                    console.log(response.results)
                    var container = $('<div class="col-sm-12 col-md-6 col-lg-3 ml-1 mr-1 mt-4"></div>').appendTo('#row');
                    var card = $('<div class="card shadow" style="border-radius: 20px"></div>').appendTo(container);
                    var col = $('<div class="col-auto"></div>').appendTo(card);
                    var img = $(`<div class="embed-responsive embed-responsive-4by3"><img class="img-fluid card-img-top embed-responsive-item" src=${product.image} style="object-fit: contain"></div>`).appendTo(col);
                    if (product.discount) {
                        var card_body = $(`<div class="card-body text-center"><h5>${product.name}</h5><p class="small text-muted text-uppercase mb-2">${product.category.name}</p><hr><h6 class="mb-3"><small class="text-grey">Real Price :<s style="font-size: 15px">${product.real_price}</s></small><br><span class="text-danger mr-1" style="font-size: 20px"><b>${product.discount_price} $</b></span></h6></div>`).appendTo(card)
                    } else {
                        var card_body = $(`<div class="card-body text-center"><h5>${product.name}</h5><p class="small text-muted text-uppercase mb-2">${product.category.name}</p><hr><p class="text-dark"><b>Price : ${product.real_price} $</b></p><br></div>`).appendTo(card)
                    }
                    if (product.inventory > 0) {
                        var add_to_cart = $(`<form  method="get"><input name="product" type="text" style="display: none" value=${product.id}><button type="submit" class="btn btn-info btn-sm mr-1 mb-2"><i class="fa fa-shopping-cart pr-2"></i>Add to cart</button></form>`).appendTo(card_body)
                        $(add_to_cart).attr('action', 'http://127.0.0.1:8000/order/add-to-cart-home-page/');
                    } else {
                        var finish = $('<button type="button" class="btn btn-secondary btn-sm mr-1 mb-2">Finished </button>')
                    }

                    var detail = $('<a class="text-dark btn btn-light btn-sm mr-1 mb-2"><i class="fa fa-info-circle pr-2"></i>Details</a>').appendTo(card_body)
                    $(detail).attr('href', '/product/detail-product/' + `${product.id}`);

                }

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
                $('#pagination').html('')
                var ul = $('<ul class="pagination pagination-large"></ul>').appendTo($('#pagination'));

                if (response.previous) {

                    var li = $('<li class="page-item"><button type="button" class="page-link">&laquo;</button></li>').appendTo(ul)
                    li.click(function () {
                        url = response.previous;
                        load_page(response.previous);
                    })
                }

                for (var i = 1; i <= response.total_pages; i++) {
                    if (response.page_number == i) {
                        $(ul).append(`<li class="active page-item"><button type="button" class="page-link" href="#" tabIndex="-1">${i}</button></li>`)
                    } else {
                        var num_li = $(`<li class="page-item"><button class="page-link" type="button">${i}</button></li>`).appendTo(ul)
                        if (response.page_number > i) {
                            num_li.click(function () {
                                url = response.previous
                                load_page(url);
                            })
                        } else {
                            num_li.click(function () {
                                url = response.next
                                load_page(url);
                            })

                        }
                    }

                }
                if (response.next) {
                    var li = $('<li class="page-item"><button type="button" class="page-link">&raquo;</button></li>').appendTo(ul)
                    li.click(function () {
                        url = response.next;
                        load_page(response.next);
                    })
                }

            }


        })

    })
}

