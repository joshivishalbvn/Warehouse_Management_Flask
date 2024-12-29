var table_id = "purchase_order_table";


$("#submit_product").on('click', function(e) {
    e.preventDefault(); // Prevent default form submission

    var product_id = $("#id_item_name").val();

    if (!product_id) {
        $.toast({
            text: 'Please select a product!',
            position: 'bottom-right',
            stack: false,
            icon: 'error',
        });
        return;
    }
    $.ajax({
        type: "GET",
        url: product_detail_url,
        data: {
            "product_id": product_id,
        },
        success: function (data) {
            if (data && data.product_data) {
                console.log("Product data received:", data.product_data);
                var productDetails = data.product_data;
                addProductRow(
                    product_id,
                    productDetails["name"],
                    productDetails["code"],
                    productDetails["case_packs"]
                );
            } else {
                console.error('Invalid data format:', data);
            }
        },
        error: function (xhr, status, error) {
            console.error("AJAX Error:", status, error);
        }
    });
});

function addProductRow(productId, productName, productCode, casePacks) {
    var productDropdownHtml = $("#id_item_name").html();
    var rowHtml = $("#product-row-template").html();

    // Replace placeholders in the rowHtml with actual index
    rowHtml = rowHtml.replace(/{index}/g, productIndex);

    // Prepend the new row to the table
    $("#product_rows").prepend(rowHtml);

    // Select the newly added row
    var newRow = $("#product_rows tr").first();
    newRow.find("select[name*='product_id']").html(productDropdownHtml);
    newRow.find("select[name*='product_id']").val(productId);
    
    // Populate case size dropdown
    populateCaseSizeDropdown(newRow.find("select[name*='case_size_id']"), casePacks);

    // Set initial values for the new row's inputs
    newRow.find("input[name*='per_piece_price']").val(""); // You can set specific default values if needed
    newRow.find("input[name*='case_quantity']").val("");
    newRow.find("input[name*='total_pieces']").val("");
    newRow.find("input[name*='item_total']").val("");

    // Increment the index for the next row
    productIndex++;

    // Update the total amount
    updateTotalAmount();
}




function populateCaseSizeDropdown(dropdown, casePacks) {
    var cases = casePacks.split('|').filter(Boolean); // Split by '|' and remove empty entries
    dropdown.empty(); // Clear existing options

    cases.forEach(function(casePack) {
        var parts = casePack.split('-');
        console.log("parts",parts)
        if (parts.length === 3) {
            var value = parts[0]; 
            var quantity = parts[1];
            var title = parts[2]; 
            var text = title;

            var optionHtml = `<option value="${value}" data-qty="${quantity}">${text}</option>`;
            dropdown.append(optionHtml);
        }
    });
}


$(document).on("click", ".button-delete", function() {
    // Get the row ID and the hidden input ID
    let row_id = $(this).data('row');
    let id = $(this).attr("value");

    // Mark the hidden input as checked
    $(id).prop('checked', true).change();

    // Hide the row
    $(row_id).addClass("d-none");

    // Update the total forms count
    let total_forms = parseInt($("#id_purchase_order_products-TOTAL_FORMS").val(), 10);
    $("#id_purchase_order_products-TOTAL_FORMS").val(total_forms - 1);

    // Check if there are no visible rows left and add a "No product found" message if needed
    let table_id = "your-table-id"; // Update this to match your actual table ID
    if ($(`#${table_id} tbody`).children("tr:not(.d-none)").length === 0) {
        $(`#${table_id} tbody`).append("<tr class='no-product'><td colspan='10'><p>No product found</p></td></tr>");
    }

    // Optionally, recalculate totals
    calculate_total(total_forms - 1);
});

