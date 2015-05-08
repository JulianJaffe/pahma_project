$(document).ready(function(){
    $('#by_location').click(function() {
        $('#range_start').attr('name', 'lo.location1');
        $('#range_end').attr('name', 'lo.location2');
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
    });
    $('#by_mus_no').click(function() {
        $('#range_start').attr('name', 'ob.objno1');
        $('#range_end').attr('name', 'ob.objno2');
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
    });

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
});