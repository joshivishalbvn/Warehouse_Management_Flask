function ajax_call_setup() {
    csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    $.ajaxSetup({
        headers: { "X-CSRFToken": csrf_token }
    });
}

function GetRevenueStatic(days){
    ajax_call_setup()
    $.ajax({
        url: url,
        type: "post",
        dataType: "json",
        data: {
            'days': days,
        },
        success: function (data) {
            $("#weekly_sold_unit").text(data["weekly_sold_unit"])
            $("#weekly_sales_orders").text(data["weekly_sales_orders"])
            $("#weekly_purchase_orders").text(data["weekly_purchase_orders"])
            $("#active_customer").text(data["active_customer"])
            $("#inactive_customer").text(data["inactive_customer"])
        },
        error: function (xhr, ajaxOptions, thrownError) {
            $.toast({
                text: "Something Went Wrong...",
                position: 'bottom-right',
                stack: false,
                icon: 'error',
            })
        }
    });
}