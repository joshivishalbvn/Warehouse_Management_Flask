
function load_zone(url) {
    var id_warehouse = document.getElementById('id_warehouse');
    var id_zone = document.getElementById('id_zone');
    id_zone.innerHTML = '';
    $.ajax({
        type: "GET",
        url: url,
        data: {
            "id_warehouse": id_warehouse.value,
        },
        success: function (data) {
            $("#id_zone").empty();

            var list = data;
            list.zone_list.forEach(element => {
                var option = document.createElement("option");
                option.value = element.id;
                option.text = element.name;
                id_zone.options.add(option);
            });
        }
    })
}