 function initailize_datatables_loading(table_id, to_center, order_false, url, columns, set_filters) {
    $(table_id).DataTable({
        scrollX: scrollX,
        columnDefs: [
            {
                targets: to_center,
                className: "text-center",
            },
            {
                orderable: false,
                targets: order_false,
            },
            {
                targets: 0,
                visible: true, // new variable true or false based on user role.
            },
        ],
        language: {
            processing: '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span>',
            "emptyTable": "No matching records found",
        },
        order: [],
        processing: true,
        serverSide: true,
        ajax: {
            url: url,
            type: 'get',
            data: set_filters(),
        },
        columns: columns,
        // rowCallback: function(nRow, aData, iDisplayIndex) {
        //     var oSettings = this.fnSettings();
        //     $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
        //     return nRow;
        // },
    });
};


function load_pending_product_table(){
    var role = true;
    var table_id = pending_loading_table
    var filter_id = $("#id_customer")
    var to_center = "_all" 
    var invisible_columns = [0]
    var order_false = [-1,0]
    var url = pending_load_url
    var columns = [
        // data: json key from prepare_results, name: model field name
        { data: 'product_details', name: 'product_details' },
        { data: 'qty', name: 'qty' },
    ]

    function set_filters() {
        var data = {}
        data["customer_id"] = $("#id_customer").val();
        return data;
    }

    initailize_datatables_loading(table_id, to_center, order_false, url, columns, set_filters);

    filter_id.on("change", function() {
        $(table_id).DataTable().destroy();
        initailize_datatables_loading(table_id, to_center, order_false, url, columns, set_filters);
    });
}

load_pending_product_table();

function load_loaded_product_table(){
    var role = true;
    var table_id = loaded_products
    var filter_id = $("#id_customer")
    var to_center = "_all" 
    var invisible_columns = [0]
    var order_false = [-1,0]
    var url = loaded_product_url
    var columns = [
        // data: json key from prepare_results, name: model field name
        { data: 'product_details', name: 'product_details' },
        { data: 'qty', name: 'qty' },
    ]

    function set_filters() {
        var data = {}
        data["customer"] = $("#id_customer").val();
        return data
    }

    initailize_datatables_loading(table_id, to_center, order_false, url, columns, set_filters);

    filter_id.on("change", function() {
        $(table_id).DataTable().destroy();
        initailize_datatables_loading(table_id, to_center, order_false, url, columns, set_filters);
    });
}

load_loaded_product_table();



function AdjustQuantity(order_product_id){
    var selected_qty = $(`#qty_${order_product_id}`).val()
    if (selected_qty=="") {
        selected_qty=0
    }
    var total_qty = $(`#totla-qty-${order_product_id}`).attr("data-qty");
    let max_val = parseInt($(`#qty_${order_product_id}`).attr("max"));

    if(max_val < total_qty){
        if(parseInt(selected_qty)>max_val){
            $(`#qty_${order_product_id}`).val(max_val);
            selected_qty = max_val;
        }
    }
    if (parseInt(selected_qty)>total_qty){
        $(`#qty_${order_product_id}`).val(total_qty);
        selected_qty = total_qty;
    }
    var new_total_qty = parseInt(total_qty) - parseInt(selected_qty)
    $(`#remaining-qty-${order_product_id}`).text(new_total_qty);

}

function ajax_call_setup() {
    csrf_token = $("#order-form input[name='csrfmiddlewaretoken']").val();
    $.ajaxSetup({
        headers: { "X-CSRFToken": csrf_token }
    });

}

function AddLoadItems(order_product_id){
    var selected_qty = $(`#qty_${order_product_id}`).val()

    if (selected_qty==0) {
        $.toast({
            text: "Please select quantity !!!",
            position: 'bottom-right',
            stack: false,
            icon: "error",
        });
    } else {
        var total_qty = $(`#totla-qty-${order_product_id}`).attr("data-qty");
        var new_total_qty = parseInt(total_qty) - parseInt(selected_qty)
        ajax_call_setup()
        $.ajax({
            url: add_item_to_loading_url,
            type: "post",
            dataType: "json",
            data: {
                'order_product_id': order_product_id,
                'total_qty': total_qty,
                'selected_qty': selected_qty,
                'new_total_qty': new_total_qty,
            },
            success: function (data) {
                $("#product_id_list").val(data.loaded_product_list)
                $(pending_loading_table).DataTable().ajax.reload(null, false);
                $(loaded_products).DataTable().ajax.reload(null, false);
                $("#submit_loading").attr("disabled",false)
                
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
}

function AdjustLoadedQuantity(loaded_product_id){
    var selected_qty = $(`#id_qty_${loaded_product_id}`).val()
    if (selected_qty=="") {
        selected_qty = 0
    }
    var loaded_qty = $(`#id_loaded-qty-${loaded_product_id}`).attr("data-qty");
    var total_qty = $(`#id-total-qty-${loaded_product_id}`).attr("data-qty");
    if (parseInt(selected_qty)>parseInt(loaded_qty)) {
        $(`#id_qty_${loaded_product_id}`).val(loaded_qty)
        var selected_qty = loaded_qty
    }
    var final_qty = parseInt(loaded_qty) - parseInt(selected_qty)
    if (parseInt(loaded_qty)>=parseInt(selected_qty)){
        $(`#id_loaded-qty-${loaded_product_id}`).text(selected_qty);
        // $(`#totla-qty-${loaded_product_id}`).text(final_qty);
    }

    $(`#id-remaining-qty-${loaded_product_id}`).text(parseInt(total_qty) + parseInt(final_qty));
}


$(document).on('click', '.loading-delete-btn', function (e) {
    var url = $(this).data("url");
    var id = $(this).data("id");
    var qty = $(`#id_qty_${id}`).val()
    ajax_call_setup()
    $.ajax({
        url: url,
        type: "post",
        dataType: "json",
        data: {
            "id": id,
            "qty": qty,
        },
        success: function (data) {
            $(pending_loading_table).DataTable().ajax.reload(null, false);
            $(loaded_products).DataTable().ajax.reload(null, false);
            if (data.is_pending_loading == false) {
                $("#submit_loading").attr("disabled",true)
            }
            
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
})

function CompleteLoading(){
    var product_ids = $("#product_id_list").val()
    var url = update_loading_ajax_url

    Swal.fire({
        html: `Are you sure you want to load this products ?`,
        icon: 'question',
        showCloseButton: true,
        showCancelButton: true,
        confirmButtonColor: "#7442DB",
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'product_ids': product_ids,
                    "csrfmiddlewaretoken": ajax_call_setup(),
                },
                success: function (data) {
                    if (data["message"]) {
                        $.toast({
                            text: data.message,
                            position: 'bottom-right',
                            stack: false,
                            icon: 'success',
                        })
                        if(data.level == "success"){
                            setTimeout(function() {
                                window.location.href = loading_complete_redirect_url;
                            }, 3000);
                        }
                    }
                }
            });
        }
    })
}