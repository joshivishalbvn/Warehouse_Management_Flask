function removeAllActiveTab(){
    $(".tab-1").removeClass("active-div");
    $(".tab-1-content").addClass("hidden");
}

$(".tab-1").click(function () {
    let id = $(this).data("id");

    removeAllActiveTab();
    $(this).addClass("active-div");
    $(this).removeClass("inactive-div");
    $(".tab-1").not(this).addClass("inactive-div");

    $(id).removeClass("hidden");
})

$(".tab-2").click(function () {
    $(this).addClass('nav-tab-active').siblings().removeClass('nav-tab-active');
    $(this).removeClass('nav-tab').siblings().addClass('nav-tab');
    
    let table_id = $(this).data('id');
    $(table_id).addClass('active').siblings().removeClass('active');
})