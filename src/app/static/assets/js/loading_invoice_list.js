function initailize_datatables_loading() {
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


var role = true;
var table_id = load_order_invoice_table
var filter_id = $("#id_order_customer,#id_order_company")
var to_center = "_all" 
var invisible_columns = [0]
var order_false = [-1,4]
var url = load_order_invoice_url
var columns = [
    // data: json key from prepare_results, name: model field name
    { data: 'invoice_id', name: 'invoice_id' },
    { data: 'customer', name: 'customer' },
    { data: 'loading_id', name: 'loading_id' },
    { data: 'total_amount', name: 'total_amount' },
    { data: 'due_amount', name: 'due_amount' },
    { data: 'action', name: 'action' },
]


function set_filters() {
    var data = {}
    data["id_order_customer"] = $("#id_order_customer").val();
    data["id_order_company"] = $("#id_order_company").val()
    return data
}
$(document).ready(function(){
    filter_id.on("change", function() {
        $(load_order_invoice_table).DataTable().destroy();
        initailize_datatables_loading()
    });
})

initailize_datatables_loading();

$(document).on('click', '.loading-list-clear', function () {
    $("#id_order_customer").val(null).trigger('change');
    $("#id_order_company").val(null).trigger('change');
})

$(document).on('click', '.add_payment', function (e) {
    var url = $(this).data("url");
    var loading_id = $(this).data("id");

    // Include loading_id in the query parameters
    var htmxUrl = url + '?loading_id=' + loading_id;

    htmx.ajax('GET', htmxUrl, {
        target: '#sidebar_form', swap: 'innerHTML'
    }).then(() => {
        $('#sidebar_form').toggleClass('sidebar-open');
    });
});


document.body.addEventListener("CreditResponse", function(evt){
    let table_id = load_order_invoice_table;
    $(document).find("#sidebar_form").removeClass('sidebar-open');
    $(table_id).DataTable().ajax.reload(null, false);

    $.toast({
        text: evt.detail.message,
        position: 'bottom-right',
        stack: false,
        icon: evt.detail.level,
    });
});

