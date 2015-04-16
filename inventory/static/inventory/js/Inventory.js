$(document).ready(function(){
    $('#by_location').click(function() {
        $('#range_start').attr('name', 'lo.location1');
        $('#range_end').attr('name', 'lo.location2');
    });
    $('#by_mus_no').click(function() {
        $('#range_start').attr('name', 'ob.objno1');
        $('#range_end').attr('name', 'ob.objno2');
    });
});