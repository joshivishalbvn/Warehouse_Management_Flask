function ajax_call_setup() {
    csrf_token = $("#order_form input[name='csrfmiddlewaretoken']").val();
    $.ajaxSetup({
      headers: { "X-CSRFToken": csrf_token }
    });

  }

function loadWarehouse() {
    var id_company = document.getElementById('id_company');
    var id_warehouse = document.getElementById('id_warehouse');
    var id_product = document.getElementById('id_product');
    var id_zone = document.getElementById('id_zone');
    id_zone.innerHTML = '';
    id_product.innerHTML = '';
    id_warehouse.innerHTML = '';
    $.ajax({
      type: "GET",
      url: "{% url 'zone:load_warehouse' %}",
      data: {
        "id_company": id_company.value,
      },
      success: function (data) {
        $("#id_warehouse").empty().append("<option value=''>-----</option>");
        $("#id_product").empty().append("<option value=''>-----</option>");

        var list = data;
        list.warehouse_list.forEach(element => {
          var option = document.createElement("option");
          option.value = element.id;
          option.text = element.name;
          id_warehouse.options.add(option);
        });
        list.product_list.forEach(element => {
          var option = document.createElement("option");
          option.value = element.id;
          option.text = element.name;
          id_product.options.add(option);
        });
      }
    })
  }


  function loadzone() {
    var id_warehouse = document.getElementById('id_warehouse');
    var id_zone = document.getElementById('id_zone');
    id_zone.innerHTML = '';
    $.ajax({
      type: "GET",
      url: "{% url 'zone:load_zone' %}",
      data: {
        "id_warehouse": id_warehouse.value,
      },
      success: function (data) {
        $("#id_zone").empty().append("<option value=''>-----</option>");

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

