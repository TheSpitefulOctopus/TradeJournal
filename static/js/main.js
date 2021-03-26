
$(document).ready(function() {
    // 
    // balance modal controls within navbar
    // 
    $('.setBalance').on("click", function () {
        $('.balanceModal').addClass('is-active');
    });
    $('.balanceModal .delete').on('click', function(){
        $('.balanceModal').removeClass('is-active');
    });

    // 
    // navbar burger controls
    //
    $('.navbar-burger').on("click", function(e){
        e.preventDefault();
        if($('.navbar-burger').hasClass('is-active')) {
            $('.navbar-burger').removeClass('is-active');
            $('.navbar-menu').removeClass('is-active');
        } else {
            $('.navbar-burger').addClass('is-active');    
            $('.navbar-menu').addClass('is-active');    
        }
        
    });

    // 
    // scroll calendar tradelist
    // 
    var curDown = false,
        curYPos = 0,
        curXPos = 0;
    $('.calendar-events').mousemove(function (m) {
        if (curDown === true) {
            $('.calendar-events').scrollTop($('.calendar-events').scrollTop() + (curYPos - m.pageY));
            $('.calendar-events').scrollLeft($('.calendar-events').scrollLeft() + (curXPos - m.pageX));
        }
    });

    $('.calendar-events').mousedown(function (m) {
        curDown = true;
        curYPos = m.pageY;
        curXPos = m.pageX;
    });

    $('.calendar-events').mouseup(function () {
        curDown = false;
    });

    $('.calendar-events').bind('selectstart dragstart', function (e) {
        e.preventDefault();
        return false;
    });





    // 
    // table
    //
    $(document).ready(function() {
        $("#editdbTable").DataTable();
    });

    // 
    // table delete
    //
    // $(document).ready(function() {
    $('.editdb').on('click', function() {
        var id = $(this).parent().siblings(":first").text()
        // alert(id);
        $.ajax({
            url: '/removeFromDb',
            data: {
                id: id
            },
            type: 'POST'
        }).done(function(data){
            console.log(data);
            location.reload()
        }).fail(function(data){
            console.log(data);
        });
    });
    // });


    // 
    // system delete
    //
    // $(document).ready(function(){
    $('.removeSystem').on('click', function() {
        var systemID = $(this).parent().parent().children(":first-child").children(":first-child").data('val');
        // console.log($(this).parent().parent().children(":first-child").children(":first-child").data('val'));
        // console.log(systemID)
        $.ajax({
            url: "/removeSystem",
            data: {
                systemID: systemID
            },
            type: 'POST'
        }).done(function(data){
            console.log(data);
            location.reload();
        }).fail(function(data){
            console.log(data)
        });
    });
    // });

});

