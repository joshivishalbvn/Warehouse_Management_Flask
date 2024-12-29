function GetRevenueStatic(days){
    $('#date_filter').addClass('d-none');
    $(table_id).DataTable().destroy();

    init_datatable(days);
    $(".tab-2").removeClass('btn-primary').addClass('btn-outline-primary');
    $(".days-"+days).addClass('btn-primary');
}

function init_datatable(days=0, custom_date=false){

    function set_filters() {
        var data = {}
        if(custom_date){
            data["date_filter"] = $("#date_range_unit").val();
        }
        data["days"] = days;
        return data;
    }

    var table = $(table_id).DataTable({
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
                targets: invisible_columns,
                visible: true,
            },
        ],
        dom: 'Bfrtip',
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
        buttons: [{
                "extend": 'excel',
                "titleAttr": 'Download Excel',
                "className" : "btn btn-primary mb-2",
                "title": title,
                "action": newexportaction,
            },
            {
                "extend": 'pdf',
                "titleAttr": 'Download PDF',
                "className" : "btn btn-primary mb-2",
                "title": title,
                "action": newexportaction,
            },
            {
                "extend": 'print',
                "titleAttr": 'Print Data',
                "className" : "btn btn-primary mb-2",
                "title": title,
                "action": newexportaction,
            },
            {
                "text": 'Clear',
                "className" : "btn btn-link mx-1 float-end",
                action: function ( e, dt, node, config ) {
                    $('#date_filter').addClass('d-none');
                    $(table_id).DataTable().destroy();
                    init_datatable(days=0);
                }
            },
            {
                "text": 'Custom',
                "className" : "btn btn-outline-primary tab-2 mx-1 float-end days-custom",
                action: function ( e, dt, node, config ) {
                    $('#date_filter').removeClass('d-none');
                    $(".tab-2").removeClass('btn-primary').addClass('btn-outline-primary');
                    $(".days-custom").addClass('btn-primary');
                }
            },
            {
                "text": '1Y',
                "className" : "btn btn-outline-primary tab-2 date_filter mx-1 float-end days-365",
                action: function ( e, dt, node, config ) {
                    GetRevenueStatic(365);
                }
            },
            {
                "text": '9M',
                "className" : "btn btn-outline-primary tab-2 date_filter mx-1 float-end days-270",
                action: function ( e, dt, node, config ) {
                    GetRevenueStatic(270);
                }
            },
            {
                "text": '6M',
                "className" : "btn btn-outline-primary tab-2 date_filter mx-1 float-end days-180",
                action: function ( e, dt, node, config ) {
                    GetRevenueStatic(180);
                }
            },
            {
                "text": '3M',
                "className" : "btn btn-outline-primary tab-2 date_filter mx-1 float-end days-90",
                action: function ( e, dt, node, config ) {
                    GetRevenueStatic(90);
                }
            },
            {
                "text": '1M',
                "className" : "btn btn-outline-primary tab-2 date_filter mx-1 float-end days-30",
                action: function ( e, dt, node, config ) {
                    GetRevenueStatic(30);
                }
            },
            {
                "text": '1W',
                "className" : "btn btn-outline-primary tab-2 date_filter mx-1 float-end days-7",
                action: function ( e, dt, node, config ) {
                    GetRevenueStatic(7);
                }
            },
        ],
        columns: columns,
        rowCallback: function(nRow, aData, iDisplayIndex) {
            var oSettings = this.fnSettings();
            $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
            return nRow;
        }
    });
    return table;
}