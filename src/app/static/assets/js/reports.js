var role = true;
	if ("{{request.user.role}}" == "Company Admin") {
		role = false;
	}
	if ("{{request.user.role}}" == "Sales Representative") {
		role = false;
	};
	var i = 1;
	var table_id = table
	var filter_id = $("#date_range")
	var to_center = "_all"
	var invisible_columns = []
	var order_false = [-1]
	var url = url
	var columns = columns

	function set_filters() {
		var data = {}
		data["date_range"] = $("#date_range").val();
		return data
	}

	initailize_datatables();