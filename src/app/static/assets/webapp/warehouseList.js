
// <!-- -------------Search Filter Js------------------- -->

$('#id_status').change(function () {
    var value = $(this).val()
    if (value == "active") {
        $(".Inactive").hide()
        $(".Active").show()
    }
    if (value == "inactive") {
        $(".Active").hide()
        $(".Inactive").show()
    }
    if (value == "All") {
        $(".Active").show()
        $(".Inactive").show()

    }
})

$(".list-clear").on("click", function () {
    $(".Active").show()
    $(".Inactive").show()
})
// <!-- -------------Search Filter Js------------------- -->


// <!-- Delete Warehouse Js -->
$(document).on('click', '.warehouse-delete-btn', function (e) {
    var id = $(this).data("id")
    var name = $(this).data("title")
    if (name == "None") {
        name = ""
    }
    var url = $(this).data("url")
    var delete_ele = $(this)


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
                    "csrfmiddlewaretoken": '{{ csrf_token }}'
                },
                success: function (data) {
                    $('#table').DataTable().ajax.reload(null, false);
                    if (data["message"]) {
                        $.toast({
                            text: data.message,
                            position: 'bottom-right',
                            stack: false,
                            icon: 'success',
                        })
                    }
                }
            });
        }
    })
})



document.body.addEventListener('htmx:beforeSwap', function (evt) {
    if (evt.detail.xhr.status === 200) {
        if (evt.detail.requestConfig.verb != 'get') {
            evt.detail.shouldSwap = false;
            window.location.reload();

        }
    }
});


// add warehouse 
$(document).on('click', '.add_warehouse', function (e) {
    url = $(this).data("url")
    htmx.ajax('GET', url, {
        target: '#sidebar_form', swap: 'innerHTML',
    }).then(() => {
        $('#sidebar_form').toggleClass('sidebar-open')

    });
})


// update warehouse 
$(document).on('click', '.update_this_warehouse', function (e) {
    url = $(this).data("url")
    htmx.ajax('GET', url, {
        target: '#sidebar_form', swap: 'innerHTML',
    }).then(() => {
        $('#sidebar_form').toggleClass('sidebar-open')

    });
})