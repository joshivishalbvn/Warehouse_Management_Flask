$(document).on('click', '.delete-btn', function (e) {
    var form = $(this);
    var id = $(this).data("id")
    var name = $(this).data("title")
    if (name == "None") {
        name = ""
    }
    var url = $(this).data("url")

    Swal.fire({
        html: `Are you sure you want to delete <b>${name}</b> ?`,
        icon: 'question',
        showCloseButton: true,
        showCancelButton: true,
        confirmButtonColor: "#7442DB",
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    "id": id,
                    "csrfmiddlewaretoken": csrf,
                },
                success: function (data) {
                    if (element_table_id == undefined){
                        location.reload();
                    }
                    else{
                        $(element_table_id).DataTable().ajax.reload(null, false);
                        if (data["message"]) {
                            $.toast({
                                text: data.message,
                                position: 'bottom-right',
                                stack: false,
                                icon: data.level ? data.level : 'success',
                            })
                        }
                    }
                }
            });
        }
    })
})



$('.delete-form').submit(function(event) {
    event.preventDefault();
    var form = $(this);
    var url = form.attr('action');

    swal({
        title: "Are you sure?",
        text: "Once deleted, you will not be able to recover this admin!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            // Perform AJAX request to delete the book
            $.ajax({
                url: url,
                method: 'POST',
                success: function(response) {
                    swal("Poof! Admin has been deleted!", {
                        icon: "success",
                    }).then(() => {
                        location.reload();  // Reload page after deletion
                    });
                },
                error: function(xhr, status, error) {
                    swal("Error", "An error occurred while deleting the admin", "error");
                }
            });
        }
    });
});