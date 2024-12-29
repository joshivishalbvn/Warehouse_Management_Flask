
function calculate_total(total_forms){
    var total_amount = 0;

    for(let i=0; i<total_forms; i++){
        if(!$("#row-"+i).hasClass("d-none")){
            let purchase_amount = parseInt($(`#id_purchase_order_products-${i}-amount`).val());
            total_amount += purchase_amount;
        }
    }
    $("#id_total_price").val(total_amount);
}

$(document).on("change", ".case_changed", function(){
    var row = $(this).data("row");
    var case_size = parseInt($(this).find(":selected").data("qty"));
    var case_qty = parseInt($(`#id_purchase_order_products-${row}-case_quantity`).val());

    var total_pieces = case_size * case_qty;
    $(`#id_purchase_order_products-${row}-total_pieces`).val(total_pieces);

    var product_price = parseInt($(`#id_purchase_order_products-${row}-per_piece_price`).val())

    $(`#id_purchase_order_products-${row}-amount`).val(product_price * total_pieces);
    
    if(window.location.href.indexOf("unload") > -1) {
        let total_unloaded = parseInt($(`#id_purchase_order_products-${row}-unloaded_pieces`).val());
        let total_delivered = 0;

        if(total_pieces > total_unloaded){
            total_delivered = total_pieces - total_unloaded;
        }
        $(`#id_purchase_order_products-${row}-undelivered_pieces`).val(total_delivered);
    }

    let total_forms = parseInt($("#id_purchase_order_products-TOTAL_FORMS").val());
    calculate_total(total_forms);
});

$(document).on("input", ".case_qty_changed", function(){
    var row = $(this).data("row");
    
    var case_qty = parseInt($(this).val());
    var case_size = parseInt($(`#id_purchase_order_products-${row}-case_size option:selected`).data("qty"));

    var total_pieces = case_size * case_qty;

    $(`#id_purchase_order_products-${row}-total_pieces`).val(total_pieces);

    var product_price = parseInt($(`#id_purchase_order_products-${row}-per_piece_price`).val());

    $(`#id_purchase_order_products-${row}-amount`).val(product_price * total_pieces);

    if(window.location.href.indexOf("unload") > -1) {
        let total_unloaded = parseInt($(`#id_purchase_order_products-${row}-unloaded_pieces`).val());
        let total_delivered = 0;

        if(total_pieces > total_unloaded){
            total_delivered = total_pieces - total_unloaded;
        }
        $(`#id_purchase_order_products-${row}-undelivered_pieces`).val(total_delivered);
    }

    let total_forms = parseInt($("#id_purchase_order_products-TOTAL_FORMS").val());
    calculate_total(total_forms);
});

$(document).on("input", ".price_changed", function(){
    var row = $(this).data("row");
    var product_price = parseInt($(this).val());
    var total_pieces = parseInt($(`#id_purchase_order_products-${row}-total_pieces`).val())

    $(`#id_purchase_order_products-${row}-amount`).val(product_price * total_pieces);

    let total_forms = parseInt($("#id_purchase_order_products-TOTAL_FORMS").val());
    calculate_total(total_forms);
});