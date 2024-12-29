
$(document).on("click", ".add-case", function(){
    row = $(this).data("row");
    let product_name = $("#id_purchase_order_products-"+row+"-product option:selected").text();
    let product_id = $("#id_purchase_order_products-"+row+"-product").val();

    $("#id_product_name").text(product_name);
    $("#id_product_case_form").find("#id_product").val(product_id);

    $("#id_product_case_form").find(".text-danger").text("");
});

$(document).on("submit", "#id_product_case_form", function(event){
    event.preventDefault();

    var is_error = false;
    var inputs = $(this).find("input");
    var url = $(this).data("url");

    for(let i in inputs){
        if(inputs[i].value == "0.0" || inputs[i].value == "0"){
            is_error = true;
            let name = inputs[i].name.replaceAll("_", " ");
            inputs[i].parentElement.getElementsByClassName("text-danger")[0].innerHTML = name+" should not be zero.";
        }
    }

    if(is_error){
        return;
    }

    var formData = new FormData(this);

    $.ajax({
        url: url,
        method: "post",
        data: formData,
        success: function(data){
            if(data.success == true){
                $('#ProductCaseForm').modal('hide');
                let text = data.product_case[1]+" Qty, "+data.product_case[2]+" Oz, "+data.product_case[3]+" CMV";
                $(`#id_purchase_order_products-${row}-case_size`).append(new Option(text, data.product_case[0]));
                $(`#id_purchase_order_products-${row}-case_size option:last`).attr("data-qty", data.product_case[1]);
                $.toast({
                    text: 'Product case created.',
                    position: 'bottom-right',
                    stack: false,
                    icon: 'success',
                });
                $("#id_product_case_form").trigger("reset");
            }
            else{
                $("#non_field_error").text(data.errors[0]);
            }
        },
        error: function (errorMessage) {
            
        },
        cache: false,
        contentType: false,
        processData: false
    });
});