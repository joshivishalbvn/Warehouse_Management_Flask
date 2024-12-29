var table;
var role = true;
if ("{{request.user.role}}" == "Company Admin") {
    role = false;
}
if ("{{request.user.role}}" == "Sales Representative") {
    role = false;
};
var i = 1;
var table_id = cart_table
var filter_id = $("#id_warehouse, #id_zone, #id_vendor")
var to_center = "_all"
var invisible_columns = []
var order_false = [1, 2, -1, -3, -4]
var url = url
var columns = [
    // data: json key from prepare_results, name: model field name
    { data: 'id', name: 'id' },
    { data: 'name', name: 'name' },
    { data: 'product_image', name: 'product_image' },
    { data: 'case_size', name: 'case_size' },
    { data: 'quantity', name: 'quantity' },
    { data: 'price', name: 'price' },
    { data: 'action', name: 'action' },
]

function set_filters() {
    var data = {}
    data["warehouse"] = $("#id_warehouse").val();
    data["zone"] = $("#id_zone").val();
    data["vendor"] = $("#id_vendor").val();
    data["product"] = $("#id_product").val();
    return data
}


function initailize_datatables() {
    table = $(table_id).DataTable({
        scrollX: true,
        columnDefs: [
            { targets: to_center, className: "text-center" },
            { orderable: false, targets: order_false },
            { targets: invisible_columns, visible: role },
        ],
        language: {
            "emptyTable": "No matching records found",
        },
        order: [],
        // Ajax for pagination
        processing: true,
        serverSide: true,
        ajax: {
            url: url,
            type: 'get',
            data: set_filters(),
        },
        columns: columns,
        rowCallback: function (nRow, aData, iDisplayIndex) {
            var oSettings = this.fnSettings();
            $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
            return nRow;
        },
    });
};
initailize_datatables();

filter_id.on("change", function () {
    $(table_id).DataTable().destroy();
    initailize_datatables();
});

// update product
$(document).on('click', '.update_product', function (e) {
    let url = $(this).data("url");

    htmx.ajax('GET', url, {
        target: '#lg_sidebar_form',
        swap: 'innerHTML',
    }).then(() => {
        $('#lg_sidebar_form').toggleClass('sidebar-open');
    });
});

$(document).on('click', '.cart-product-delete-btn', function (e) {
    var id = $(this).data("id")
    var name = $(this).data("title")
    if (name == "None") {
        name = ""
    }
    var delete_url = $(this).data("url");

    Swal.fire({
        html: `Are you sure you want to delete <b>${name}</b> ?`,
        icon: 'question',
        showCloseButton: true,
        showCancelButton: true,
        confirmButtonColor: "#7442DB",  
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: "POST",
                url: delete_url,
                data: {
                    "id": id,
                    "csrfmiddlewaretoken": csrf,
                },
                success: function (data) {
                    table.ajax.reload(null, false);
                }
            });
        }
    })
})

function ajax_call_setup() {
    csrf_token = $("#order_form input[name='csrfmiddlewaretoken']").val();
    console.log({ csrf_token })
    $.ajaxSetup({
        headers: { "X-CSRFToken": csrf_token }
    });

}

function CopyBillindAdd() {
   var suit_appartmnet = $("#id_shipping_address_suite_apartment").val()
   var address_line_1 = $("#id_shipping_address_line_1").val()
   var address_line_2 = $("#id_shipping_address_line_2").val()
   var shipping_city = $("#id_shipping_city").val()
   var shipping_state = $("#id_shipping_state").val()
   var shipping_country = $("#id_shipping_country").val()
   var shipping_zip_code = $("#id_shipping_zip_code").val()

   $("#id_billing_address_suite_apartment").val(suit_appartmnet)
   $("#id_billing_address_line_1").val(address_line_1)
   $("#id_billing_address_line_2").val(address_line_2)
   $("#id_billing_city").val(shipping_city)
   $("#id_billing_state").val(shipping_state)
   $("#id_billing_country").val(shipping_country)
   $("#id_billing_zip_code").val(shipping_zip_code)

}