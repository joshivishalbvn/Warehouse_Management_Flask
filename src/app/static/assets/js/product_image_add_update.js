//<!--upload multiple image show-->


var img_count = 0
var image_count = 0

// Multiple images preview in browser
function imagesPreview(input, placeToInsertImagePreview) {
    if (input.files) {
        var filesAmount = input.files.length; 

        img_count += filesAmount
        if ($("#image_count").val()){
            image_count = parseInt($("#image_count").val());    
        }
        var total_image_count = parseInt(image_count) + parseInt(img_count);
        if (total_image_count > 5){
            image_count =  0
            img_count = 0
            total_image_count = 0
            $("#error_message").empty()
            $("#error_message").append("<span style='color:red;'>Note: You can select upto 5 images.</span>")
            $("#id_product_image").val("");
            $('.selected_images').remove() 
            total_image_count = 0
            
        }
        else {
            //$('.selected_images').remove()
            $("#error_message").empty("");
            for (let i = 0; i < filesAmount; i++) {
                var reader = new FileReader();
                reader.onload = function (event) {
                    $($.parseHTML(`<div class="image col-lg-4 selected_images" data-id=${filesAmount} id="image_id_${i}">
                        <img class="btn-delete selected_product_image_delete"
                            data-source="${event.target.result}"
                            data-id="${i}"
                            src="http://cdn1.iconfinder.com/data/icons/diagona/icon/16/101.png" /><img id="photo_${i}" src="${event.target.result}">`)).appendTo(placeToInsertImagePreview);
                }
                reader.readAsDataURL(input.files[i]);
            }
        }
    }
};

function imagesPreview2(input, placeToInsertImagePreview) {
    if (input.files) {
        var filesAmount = input.files.length; 

        img_count += filesAmount
        if ($("#image_count").val()){
            image_count = parseInt($("#image_count").val());    
        }
        var total_image_count = parseInt(image_count) + parseInt(img_count);
        if (total_image_count > 5){
            image_count =  0
            img_count = 0
            total_image_count = 0
            $("#error_message").empty()
            $("#error_message").append("<span style='color:red;'>Note: You can select upto 5 images.</span>")
            $("#id_product_image").val("");
            $('.selected_images').remove() 
            total_image_count = 0
            
        }
        else {
            //$('.selected_images').remove()
            $("#error_message").empty("");
            for (let i = 0; i < filesAmount; i++) {
                var reader = new FileReader();
                reader.onload = function (event) {
                    $($.parseHTML(`<div class="image"><img src="${event.target.result}" width=100%>`)).appendTo(placeToInsertImagePreview);
                }
                reader.readAsDataURL(input.files[i]);
            }
        }
    }
};