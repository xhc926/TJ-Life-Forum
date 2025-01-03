import './jquery-1.8.3.min.js';
$(document).ready(function() {
    //nav     
    var obj = null;
    var obj = null;
    var starlist = document.getElementById('starlist');
    if (starlist) {
        var As = starlist.getElementsByTagName('a');
        obj = As[0];
        for (let i = 1; i < As.length; i++) {
            if (window.location.href.indexOf(As[i].href) >= 0) obj = As[i];
        }
        obj.id = 'selected';
    }
    //nav
    $("#mnavh").click(function() {
        $("#starlist").toggle();
        $("#mnavh").toggleClass("open");
    });
    //search  
    $(".searchico").click(function() {
        $(".search").toggleClass("open");
    });
    //searchclose 
    $(".searchclose").click(function() {
        $(".search").removeClass("open");
    });
    //banner
    $('#banner').easyFader();
    //nav menu   
    $(".menu").click(function(event) {
        $(this).children('.sub').slideToggle();
    });
    //tab
    $('.tab_buttons li').click(function() {
        $(this).addClass('newscurrent').siblings().removeClass('newscurrent');
        $('.newstab>div:eq(' + $(this).index() + ')').show().siblings().hide();
    });
});