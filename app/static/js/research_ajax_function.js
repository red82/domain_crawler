
var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //AJAX POST request get research
    $(document).ready(function(){

        $("#id_catalog").on('change', function(){
            console.log("Start");
            var field = $("#id_catalog")[0];
            var input_string = field.options[field.selectedIndex].text;
            console.log("input_string", input_string);
            $.ajax({
                url : "/ajax_research_request",
                type : "POST",
                dataType: "json",
                data : {
                    client_response : input_string,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success : function(json) {
                console.log('json=', json);
                $('#result').append(json);
                },
                error : function(xhr,errmsg,err) {
                    alert(xhr.status + ": " + xhr.responseText);
                }
            });
            return false;
        });
    });
