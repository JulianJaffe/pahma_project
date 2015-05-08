$(document).ready(function(){
$('[name]').map(function () {
    var elementID = $(this).attr('name');
    var source = $(this).attr('source');
    if (source) {
        // console.log(elementID);
        $(this).autocomplete({
            source: function (request, response) {
                $.ajax({
                     url: "/pahma_project/suggest/?",
                     dataType: "json",
                    data: {
                        q: request.term,
                        elementID: elementID,
                        source: source
                    },
                    success: function (data) {
                        response(data);
                    }
                });
            },
            minLength: 2
        });
    }
});
    if($('#by_crate').is(':checked')){
        $('.td-by_obj_no').prop('disabled', true).hide();
        $('.td-by_crate').show();
    }

    if($('#by_obj_no').is(':checked')){
        $('.td-by_crate').prop('disabled', true).hide();
        $('.td-by_obj_no').show();
    }

    $('input[name=move_type]:radio').change(function() {
        if(this.value == 'by_obj_no') {
            $('.td-by_crate').prop('disabled', true).hide();
            $('.td-by_obj_no').prop('disabled', false).show();
        } else {
            $('.td-by_obj_no').prop('disabled', true).hide();
            $('.td-by_crate').prop('disabled', false).show();
        }
    });
});
