// <!-- -------------Search Filter Js------------------- -->
$('#id_status').change(function () {
    var value = $(this).val()

    if (value == "Active") {
        $(".Inactive").hide()
        $(".Active").show()
    }
    if (value == "Inactive") {
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
    $("#id_status").val("All").trigger('change');
})
// <!-- -------------Search Filter Js------------------- -->




document.body.addEventListener('htmx:beforeSwap', function (evt) {
    if (evt.detail.xhr.status === 200) {
        if (evt.detail.requestConfig.verb != 'get') {
            evt.detail.shouldSwap = false;
            window.location.reload();

        }
    }
});



// update company 
$(document).on('click', '.open_sidebar', function (e) {
    url = $(this).data("url")
    htmx.ajax('GET', url, {
        target: '#sidebar_form', swap: 'innerHTML',
    }).then(() => {
        $('#sidebar_form').toggleClass('sidebar-open')

    });
})



$("#sidebar_form").attr('style', 'width: 25%');



function open_file() {
    $("#id_company_logo_upload").click();
}




if (document.getElementById('image-preview').getAttribute('src') == "/static/images/default-profile.png") {
    $("#clear-btn").hide()
} else {
    $("#clear-btn").show()
}
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("image-preview").src = e.target.result;
        }
        $("#clear-btn").show()
        checkBox = document.getElementById('image-clear');
        reader.readAsDataURL(input.files[0]);
    }
    else {
        $("#image").empty()
    }
}
$("#id_logo").on("change", function () {
    readURL(this);
})
$("#clear-btn").on("click", function () {
    $("#id_logo").val("");
    checkBox = document.getElementById('image-clear');
    checkBox.checked = true;
    document.getElementById("image-preview").src = "{% static 'images/default-profile.png' %}";
    $("#clear-btn").hide()
})


$('#id_status').select2({
    width: "100%",
});


function open_file() {
    document.getElementById('id_logo').click();
  }

  document.getElementById('id_logo').addEventListener('change', function() {
    var preview = document.getElementById('image-preview');
    var file = this.files[0];
    var reader = new FileReader();

    reader.onloadend = function() {
      preview.src = reader.result;
    };
    if (file) {
      reader.readAsDataURL(file);
    } else {
      preview.src = "";
    }
  });