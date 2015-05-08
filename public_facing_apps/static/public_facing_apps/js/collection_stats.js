$(document).ready(function () {

    $('input:text:first').focus();

    $(function() {
      $('[id^="sortTable"]').map(function() {
            // console.log(this);
            $(this).tablesorter({debug: true})
         });
      });

    $(".dashboardcell").click(function() {
            var paneid = $(this).attr('id') + 'pane';
            $('#' + paneid).show();
            $('#overlay').show();
        });
        $(".close").click(function() {
            var closeid = $(this).attr('id').replace("close","pane");
            $('#' + closeid).hide();
            $('#overlay').hide();
        });
        $(".selimg").click(function() {
            var showid = $(this).attr('id').replace("sel","");
            if(showid.indexOf("close") != -1) {
                        var closeid = showid.replace("close","pane");
                        $('#' + closeid).hide();
                        $('#overlay').hide();
            } else if(showid.indexOf("chart") != -1) {
                $('#' + showid.replace("chart", "table")).hide();
                $('#' + showid.replace("chart", "time")).hide();
                if (document.getElementById(showid).style.display == 'none'){
                    $('#' + showid).show(0)
                } //else {
                    //$('#' + showid).hide();
                //}
            } else if(showid.indexOf("table") != -1) {
                $('#' + showid.replace("table", "chart")).hide();
                $('#' + showid.replace("table", "time")).hide();
                $('#' + showid).show(0)
            } else if(showid.indexOf("time") != -1) {
                $('#' + showid.replace("time", "chart")).hide();
                $('#' + showid.replace("time", "table")).hide();
                $('#' + showid).show(0)
            }
        });
});
