$(document).ready(function () {
    var counter = 0
   
    $("#submit_product").on('click', function (e) {
        var product_id = $(id_item_name).val();
        var table_id = "purchase_order_table"
        var url= "{% url 'purchase_order:get_product_ajax' %}"

        if ($('#purchase_order_table').has('.no-product-row').length > 0) {
            $('.no-product-row').remove();
        }

        $.ajax({
            type: "GET",
            url: url,
            data: {
                "product_id": product_id,
            },
            success: function (data) {
                var productDetailUrl = "{% url 'products:product_details' $(product_id) %}".replace('0', data.id);
                var action = `<a href="${productDetailUrl}"><i class="fa fa-eye font-medium-3 mr-2"></i></a>
                        <a href=""><i class="fa fa-edit font-medium-3 mr-2"></i></a>
                        <span class="row_delete_btn" data-id="${counter}" style="cursor: pointer;"><i class="fa fa-trash font-medium-3 mr-2"></i></span>`
                $(`#${table_id} tbody`).append(`<tr id ="table_row_${counter}"><td class='text-center'><a href="${productDetailUrl}" >${data.code} </a> </td><td class='text-center'> ${data.name} </td><td class='text-center'>  <input class="form-control" type="Number" min=0 value="24"> </td><td class='text-center'>  <input class="form-control" type="Number" min=0 value="22"> </td><td class='text-center'>  <input class="form-control" type="Number" min=0 value="100"> </td><td class='text-center'>  <input class="form-control" type="Number" min=0 value="2541"> </td><td class='text-center'> ${action} </td></tr>`);
            }
        })
        counter += 1;
    });

    function format(product) {
        if (!product.id) return product.text;
        var $product = $(
            '<div class="row">'+
            '<div class="col-1">'+
            '<img src="'+$(product.element).data('image')+'" class="dropdown-image" />' +
            '</div>'+
            '<div class="col-11">'+
            '<div class="">' + product.text + '</div>' +
            '</div>'+
            '</div>');
        return $product;
    }

    $('#id_item_name').select2({
        templateResult: format,
        placeholder: "Choose Item",
    });

    function calculate_purchase_order_total() {
            purchase_order_sum = 0;
            product_prices = [];
            $(".product-total-price").each(function () {
                product_prices.push(parseFloat($(this).val()));
            });
            purchase_order_sum = product_prices.reduce((sum, a) => sum + a, 0);
            $("#form_purchase_order #id_total_price ").val(purchase_order_sum.toFixed(2));
        }

    $(document).on("click",".row_delete_btn", function(){
        row_id = $(this).data('id')
        $(`#table_row_${row_id}`).remove();
    });
});
