
function AddToCart($this) {
    var product_id = $this;
    var quantity = $(`#qty-${product_id}`).val()
    var case_size = $(`#cases-${product_id}`).val()
    if (quantity==0) {
        alert("Please select quantity")
    } else {
        if (case_size == 0) {
            alert("Please select case size")
        } else {
            $.ajax({
                url: add_order_url,
                type: "get",
                dataType: "json",
                data: {
                    'product_id': product_id,
                    'case_size': case_size,
                    'quantity': quantity,
                },
                success: function (data) {
                    $(".cart-items-count").text(data.order_qty)
                    $(`#qty-${product_id}`).val(0)
                    $(`#cases-${product_id}`).val(0)
                    $.toast({
                        text: "Order Added To Cart...",
                        position: 'bottom-right',
                        stack: false,
                        icon: 'success',
                    })
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(thrownError);
                    $.toast({
                        text: "Something Went Wrong...",
                        position: 'bottom-right',
                        stack: false,
                        icon: 'error',
                    })
                }
            });
        }
    }
}
