function validate_discount(percent){
    if(percent > 100){
        $(this).val(100);
    }
    else if(percent < 0){
        $(this).val(0);
    }
}

function calculate_grand_total(){
    var packing_charge = parseInt($("#id_packing_charge").val());
    var shipping_charge = parseInt($("#id_shipping_charge").val());
    var total_amount = parseInt($("#id_total_amount").val());
    var discount_per = parseFloat($("#id_discount").val());

    var discount_amt = total_amount * (discount_per / 100);
    
    $(`#id_adjustments`).val(discount_amt);
    $(`#id_grand_total`).val((total_amount - discount_amt) + packing_charge + shipping_charge);
}

function calculate_total(total_forms){
    var total_amount = 0;

    for(let i=0; i<total_forms; i++){
        if(!$("#row-"+i).hasClass("d-none")){
            let sale_amount = parseInt($(`#id_orders-${i}-net_price`).val());
            total_amount += sale_amount;
        }
    }
    $("#id_total_amount").val(total_amount);

    calculate_grand_total();
}

$(document).on("change", ".case_changed", function(){
    var row = $(this).data("row");
    var case_pack = parseInt($(this).find(":selected").data("qty"));
    var case_qty = parseInt($(`#id_orders-${row}-quantity`).val());

    var total_pieces = case_pack * case_qty;
    $(`#id_orders-${row}-total_pieces`).val(total_pieces);

    var product_price = parseInt($(`#id_orders-${row}-customer_price`).val())
    var item_total = product_price * total_pieces
    $(`#id_orders-${row}-item_total`).val(item_total);

    var discount_per = parseFloat($(`#id_orders-${row}-discount`).val());
    var discount_amt = item_total * (discount_per / 100)
    $(`#id_orders-${row}-net_price`).val(item_total - discount_amt);

    let total_forms = parseInt($("#id_orders-TOTAL_FORMS").val());
    calculate_total(total_forms);
});

$(document).on("input", ".case_qty_changed", function(){
    var row = $(this).data("row");
    
    var case_qty = parseInt($(this).val());
    var case_pack = parseInt($(`#id_orders-${row}-case_pack option:selected`).data("qty"));

    var total_pieces = case_pack * case_qty;

    $(`#id_orders-${row}-total_pieces`).val(total_pieces);

    var product_price = parseInt($(`#id_orders-${row}-customer_price`).val());
    var item_total = product_price * total_pieces;
    $(`#id_orders-${row}-item_total`).val(item_total);

    var discount_per = parseFloat($(`#id_orders-${row}-discount`).val());
    var discount_amt = item_total * (discount_per / 100);
    $(`#id_orders-${row}-net_price`).val(item_total - discount_amt);

    let total_forms = parseInt($("#id_orders-TOTAL_FORMS").val());
    calculate_total(total_forms);
});

// $(document).on("input", ".change_discount", function(){
//     var row = $(this).data("row");
//     var discount_per = parseFloat($(this).val());

//     validate_discount(discount_per);

//     var item_total = parseInt($(`#id_orders-${row}-item_total`).val());

//     var discount_amt = item_total * (discount_per / 100);
//     $(`#id_orders-${row}-net_price`).val(item_total - discount_amt);

//     let total_forms = parseInt($("#id_orders-TOTAL_FORMS").val());
//     calculate_total(total_forms);
// });

// when select discount in %
// $('#id_discount').on('input', function() {
//     let total_amount = parseInt($("#id_total_amount").val());
//     var packing_charge = parseInt($("#id_packing_charge").val());
//     var shipping_charge = parseInt($("#id_shipping_charge").val());
//     let discount = parseFloat($(this).val());
    
//     validate_discount(discount);

//     let discount_amount = total_amount*(discount/100);
//     $('#id_adjustments').val(discount_amount);

//     $("#id_grand_total").val((total_amount - discount_amount) + packing_charge + shipping_charge);
//   });

// when select discount in $
// $('#id_adjustments').on('input', function() {
//     let total_amount = parseInt($("#id_total_amount").val());
//     var packing_charge = parseInt($("#id_packing_charge").val());
//     var shipping_charge = parseInt($("#id_shipping_charge").val());
//     let discount = parseInt($(this).val());

//     if(discount > total_amount){
//         $(this).val(total_amount);
//     }

//     let discount_percentage = ((discount/total_amount)*100).toFixed(2);
//     $('#id_discount').val(discount_percentage);
//     $("#id_grand_total").val((total_amount - discount) + packing_charge + shipping_charge);
// });

// $(document).on("input", "#id_packing_charge, #id_shipping_charge", function(){
//     let total_amount = parseInt($("#id_total_amount").val());
//     var packing_charge = parseInt($("#id_packing_charge").val());
//     var shipping_charge = parseInt($("#id_shipping_charge").val());
//     let discount = parseFloat($("#id_discount").val());
//     let discount_amount = total_amount*(discount/100);
//     $('#id_adjustments').val(discount_amount);

//     $("#id_grand_total").val((total_amount - discount_amount) + packing_charge + shipping_charge);
// });