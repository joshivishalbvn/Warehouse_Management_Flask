
function format(product) {
    if (!product.id) return product.text;
    let image = $(product.element).data('image')
    
    if (image == undefined){
        image = product.image;
    }
    var $product = $(
        '<div class="row">'+
        '<div class="col-2 col-md-2 text-center">'+
        '<img src="'+image+'" height="35px" />' +
        '</div>'+
        '<div class="col-10 col-md-10 px-auto">'+
        '<div class="">' + product.text + '</div>' +
        '</div>'+
        '</div>');
    return $product;
}

function product_dropdown(product_id, sales_order=false, company){
    $(product_id).select2({
        placeholder: "Search by product code, name and barcode",
        templateResult: format,
        allowClear: true,
        ajax: {
            url: product_search_url,
            data: function (params) {
                var query = {
                    search: params.term,
                    type: 'public'
                }
                if(company){
                    query["company"] = $(company).val();
                }
                if(sales_order){
                    let customer_id = $("#id_customer").val()
                    console.log(customer_id);
                    if(customer_id){
                        query["customer_id"] = customer_id;
                    }
                    else{
                        query["customer_id"] = 0;
                    }
                }
                return query;
            },
            processResults: function (data) {
                return {
                  results: data.items
                };
            },
        },
    });
}