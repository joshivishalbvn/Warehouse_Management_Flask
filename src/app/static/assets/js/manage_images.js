function imagesPreview(input, placeToInsertImagePreview) {
    if (input.files) {
        var reader = new FileReader();
        reader.onload = function(event) {
            if (input.files[0].type.includes('image')) {
                var imageHTML = `<div class="image col-lg-2 selected_images" id="image_id">
                                    <img class="btn-delete selected_image_delete"
                                        data-source="${event.target.result}"
                                        data-id=""
                                        src="http://cdn1.iconfinder.com/data/icons/diagona/icon/16/101.png" />
                                    <img id="photo" src="${event.target.result}">
                                    <p>${input.files[0].name}</p>
                                </div>`;
                $(placeToInsertImagePreview).html(imageHTML);
            } else if (input.files[0].type.includes('pdf')) {
                var pdfHTML = `<div class="image col-lg-2 selected_images" id="image_id">
                                    <img class="btn-delete selected_image_delete"
                                        data-source="${event.target.result}"
                                        data-id=""
                                        src="http://cdn1.iconfinder.com/data/icons/diagona/icon/16/101.png" />
                                    <img id="photo" src="/static/photos/jobwork/pdf.png">
                                    <p>${input.files[0].name}</p>
                                </div>`;
                $(placeToInsertImagePreview).html(pdfHTML);
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function manage_images(id, target_to_display){
    $(id).on('change', function () {
        imagesPreview(this, target_to_display);
    });
}

$(document).on("click", ".selected_image_delete", function(){
    var image_src = $(this).data('source');

    if (image_src){
        image_src = "/static/photos/jobwork/pdf.png"
    }
    else{
        image_src = $(this).data('source')
    }

    Swal.fire({
        html: `Are you sure you want to delete Invoice ?`,
        iconHtml: `<img src=${image_src}>`,
        showCloseButton: true,
        showCancelButton: true,
        confirmButtonColor: "#7442DB",
    }).then((result) => {
        if (result.isConfirmed) {
            $(`#image_id`).remove()
            $('.selected_images').remove()
            $('#id_invoice').val("");
            img_count = 0;

            $.toast({
                text: "Invoice Deleted Successfully",
                position: 'bottom-right',
                stack: false,
                icon: 'success',
            });
        }
    });
});

$(document).on('click', '.product_image_delete', function (e) {
    var photo_id = $(this).data("id");
    var url = $(this).data("url");
    var csrf = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        type: "POST",
        url: url,
        data: {
            "photo_id": photo_id,
            "csrfmiddlewaretoken": csrf,
        },
        success: function (data) {
            $(`#image_id_${photo_id}`).remove();
            $.toast({
                text: data.message,
                position: 'bottom-right',
                stack: false,
                icon: 'success',
            });
        }
    });
});