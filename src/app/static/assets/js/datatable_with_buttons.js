function initailize_datatables() {
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
        dom: 'Bfrtip',
        buttons: [
            {
                "extend": 'excel',
                "titleAttr": 'Download Excel',
                "className" : "btn btn-primary mb-2",
                "title": title,
                "action": newexportaction,
                // "exportOptions": {
                //     columns: ':not(:last-child)',
                // },
            },
            {
                "extend": 'pdf',
                "titleAttr": 'Download PDF',
                "className" : "btn btn-primary mb-2",
                "title": title,
                "action": newexportaction,
                // "exportOptions": {
                //     columns: ':not(:last-child)',
                // },
            },
            {
                "extend": 'print',
                "titleAttr": 'Print Data',
                "className" : "btn btn-primary mb-2",
                "title": title,
                "action": newexportaction,
                // "exportOptions": {
                //     columns: ':not(:last-child)',
                // },
            },
        ],
        columns: columns,
        // rowCallback: function(nRow, aData, iDisplayIndex) {
        //     var oSettings = this.fnSettings();
        //     $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
        //     return nRow;
        // },
    });
};


function newexportaction(e, dt, button, config) {
    var self = this;
    var oldStart = dt.settings()[0]._iDisplayStart;
    dt.one('preXhr', function (e, s, data) {
        // Just this once, load all data from the server...
        data.start = 0;
        data.length = 2147483647;
        dt.one('preDraw', function (e, settings) {
            // Call the original action function
            if (button[0].className.indexOf('buttons-copy') >= 0) {
                $.fn.dataTable.ext.buttons.copyHtml5.action.call(self, e, dt, button, config);
            } else if (button[0].className.indexOf('buttons-excel') >= 0) {
                $.fn.dataTable.ext.buttons.excelHtml5.available(dt, config) ?
                    $.fn.dataTable.ext.buttons.excelHtml5.action.call(self, e, dt, button, config) :
                    $.fn.dataTable.ext.buttons.excelFlash.action.call(self, e, dt, button, config);
            } else if (button[0].className.indexOf('buttons-csv') >= 0) {
                $.fn.dataTable.ext.buttons.csvHtml5.available(dt, config) ?
                    $.fn.dataTable.ext.buttons.csvHtml5.action.call(self, e, dt, button, config) :
                    $.fn.dataTable.ext.buttons.csvFlash.action.call(self, e, dt, button, config);
            } else if (button[0].className.indexOf('buttons-pdf') >= 0) {
                $.fn.dataTable.ext.buttons.pdfHtml5.available(dt, config) ?
                    $.fn.dataTable.ext.buttons.pdfHtml5.action.call(self, e, dt, button, config) :
                    $.fn.dataTable.ext.buttons.pdfFlash.action.call(self, e, dt, button, config);
            } else if (button[0].className.indexOf('buttons-print') >= 0) {
                $.fn.dataTable.ext.buttons.print.action(e, dt, button, config);
            }
            dt.one('preXhr', function (e, s, data) {
                // DataTables thinks the first item displayed is index 0, but we're not drawing that.
                // Set the property to what it was before exporting.
                settings._iDisplayStart = oldStart;
                data.start = oldStart;
            });
            // Reload the grid with the original page. Otherwise, API functions like table.cell(this) don't work properly.
            setTimeout(dt.ajax.reload, 0);
            // Prevent rendering of the full data to the DOM
            return false;
        });
    });
    // Requery the server with the new one-time export settings
    dt.ajax.reload();
};