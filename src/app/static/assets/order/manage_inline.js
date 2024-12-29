var table_id = "order_table";

$("#submit_product").on('click', function(e){
    var product_id = $("#id_item_name").val();
    if(!product_id){
        $.toast({
            text: 'No product selected !!!',
            position: 'bottom-right',
            stack: false,
            icon: 'error',
        });
        return;
    }

    var case_packs = "";
    var product_name = "";
    var product_code = "";
    var product_price = "";

    $.ajax({
        type: "GET",
        url: product_detail_url,
        data: {
            "product_id": product_id,
            "type": "sales_order",
        },
        success: function (data) {
            product_name = String(data.product_data["name"]);
            product_code = String(data.product_data["code"]);
            case_packs = String(data.product_data["case_packs"]);
            product_price = String(data.product_data["product_price"]);
        }
    }).then(()=>{
    
        var total_forms = parseInt($("#id_orders-TOTAL_FORMS").val());

        if ($(`#${table_id}`).has('.no-product').length > 0) {
            $('.no-product').remove();
        }

        let clone_group = $(".extra-fields-wrap").first().html();
        
        let _html_text = clone_group.replaceAll("__prefix__", total_forms);
        let row = $.parseHTML(_html_text);
        
        if(case_packs != ""){
            case_packs = case_packs.split("|");
        }

        let product_detail_url = productDetailUrl.replace('0', product_id);
        $(row).find(`#row-${total_forms}-product_name`).text(product_name);
        $(row).find(`#row-${total_forms}-product_code`).attr("href", product_detail_url).text(product_code);
        
        $(row).find(`#id_orders-${total_forms}-case_pack`).attr("data-row", total_forms);
        $(row).find(`#id_orders-${total_forms}-quantity`).attr("data-row", total_forms);
        $(row).find(`#id_orders-${total_forms}-customer_price`).attr("data-row", total_forms);
        $(row).find(`#id_orders-${total_forms}-discount`).attr("data-row", total_forms);
        $(row).find(`#id_orders-${total_forms}-case_pack`).find('option').remove();
        
        for(let i=0; i<case_packs.length-1; i++){
            let id = case_packs[i].split("-")[0];
            let qty = case_packs[i].split("-")[1];
            let text = case_packs[i].split("-")[2];

            $(row).find(`#id_orders-${total_forms}-case_pack`).append(new Option(text, id));
            $(row).find(`#id_orders-${total_forms}-case_pack option:last`).attr("data-qty", qty);
        }
        
        $(`#${table_id} tbody`).prepend(row);
        $("#row-" + total_forms).find(".form-control").val(0);

        $(`#id_orders-${total_forms}-case_pack`).prop("selectedIndex", 0);
        $(`#id_orders-${total_forms}-product`).val(product_id);
        $(`#id_orders-${total_forms}-customer_price`).val(product_price);

        $(`#id_orders-${total_forms}-quantity`).focus();
        
        total_forms++;
        $("#id_orders-TOTAL_FORMS").val(total_forms);
    });
});

$(document).on("click", ".button-delete", function(){
    let row_id = $(this).data('row');
    let id = $(this).attr("value");
    
    $(id).attr('checked', "true").change();
    let total_forms = parseInt($("#id_orders-TOTAL_FORMS").val());

    $(row_id).addClass("d-none");
    if($(`#${table_id} tbody`).children("tr:not(.d-none)").length == 0){
        $(`#${table_id} tbody`).append("<tr class='no-product'><td colspan='10'><p>No product found</p></td></tr>");
    }
    
    calculate_total(total_forms);
});