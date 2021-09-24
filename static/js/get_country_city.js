$(document).ready(function () {
    //Call restful countries country endpoint
    //https://restcountries.eu/rest/v2/all
    $.get('https://countriesnow.space/api/v0.1/countries/', function (countries) {
        for (let data of countries.data) {
            $('#country-select')
                .append($("<option></option>")
                    .attr("value", data.country)
                    .text(data.country));
        }

    });
});

//Function to fetch states
function initStates() {
    //Get selected country name
    let country = $("#country-select").val();

    //Remove previous loaded states
    $('#state-select option:gt(0)').remove();


    //Call restful countries states endpoint
    $.ajax({
        url: 'https://countriesnow.space/api/v0.1/countries/states',
        type: 'POST',
        data: {"country": country.toLowerCase(), "order": "asc", "orderBy": "name"},
        success: function (result) {

            for (let city of result.data.states) {
                $('#state-select')
                    .append($("<option></option>")
                        .attr("value", city.name.split("Province")[0])
                        .text(city.name.split("Province")[0]));

            }
        },
        error: function () {
            alert('Please refresh the webpage')
        }
    })
}