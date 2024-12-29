var role = true;
if ("{{request.user.role}}" == "company admin") {
    role = false;
}
if ("{{request.user.role}}" == "sales representative") {
    role = false;
};
var i = 1;
var table_id = table_id
var filter_id = $("");
var to_center = "_all"
var invisible_columns = []
var order_false = [-1]
var url = url


var columns = [
    // data: json key from prepare_results, name: model field name
    { data: 'id', name: 'id' },
    { data: 'product', name: 'product' },
    { data: 'quantity', name: 'quantity' },
    { data: 'case_pack', name: 'case_pack' },
    { data: 'unit_price', name: 'unit_price' },
    { data: 'item_total', name: 'item_total' },
    { data: 'discount', name: 'discount' },
    { data: 'net_price', name: 'net_price' },
]

function set_filters() {
    var data = {}
    data["loading_order_id"] = load_order_id
    return data;
}

initailize_datatables();