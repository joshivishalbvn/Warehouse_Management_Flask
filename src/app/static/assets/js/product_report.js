var role = true;
if ("{{request.user.role}}" == "Company Admin") {
	role = false;
}
if ("{{request.user.role}}" == "Sales Representative") {
	role = false;
};
var i = 1;
var table_id = table_id
var filter_id = $("#id_company,#id_role")
var to_center = "_all"
var invisible_columns = []
var order_false = [2, 3, 4, 5, 6, -1]
var url = url
var columns = [
	// data: json key from prepare_results, name: model field name
	{ data: 'warehouse', name: 'warehouse' },
	{ data: 'product', name: 'product' },
	{ data: 'stock_sitting', name: 'stock_sitting' },
	{ data: 'total_qty', name: 'total_qty' },
	{ data: 'locked_qty', name: 'locked_qty' },
	{ data: 'saleable_qty', name: 'saleable_qty' },
	{ data: 'previouse_cost', name: 'previouse_cost' },
	{ data: 'current_cost', name: 'current_cost' },
]
function set_filters() {
	var data = {}
	data["company"] = $("#id_company").val();
	data["role"] = $("#id_role").val();
	return data
}

initailize_datatables();

$(document).on('click', '.list-clear', function () {
	$("#id_company").val(null).trigger('change');
	$("#id_role").val(null).trigger('change');
})