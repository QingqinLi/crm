// $('.title').click(function(){
// //     $(this).next().toggleClass('hide');
// // });
$('.title').click(function () {
    $(this).next().removeClass('hide');
    $(this).parent().siblings().find('.body').addClass('hide');
});