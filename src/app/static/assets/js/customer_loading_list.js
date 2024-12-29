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
var table_id = customer_loading_list_table_id
var filter_id = $("#id_order_customer,#id_order_company")
var to_center = "_all" 
var invisible_columns = [0]
var order_false = [-1, 1]
var url = customer_loading_list_url
var columns = [
    { data: 'loading_id', name: 'loading_id' },
    { data: 'orders', name: 'orders' },
    { data: 'grand_total', name: 'grand_total' },
    { data: 'status', name: 'status' },
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
        $(loading_list_table_id).DataTable().destroy();
        initailize_datatables_loading()
    });
})


initailize_datatables_loading();