/**
 * Created by dingwenkai on 16/10/11.
 */
$(document).ready(function (){
    $.ajax({
        type: "GET",
        url: "/get_newpage_info",
        success:function(html){
            $(".tbody").empty();
            $(".tbody").append(html)
        }
    });
    $("#create_script").click(function(){
        var script_info = $(".script_info_new").val();
        var script_path = $(".script_path_new").val();
        var data=
                {
                    "script_info": script_info,
                    "script_path": script_path
                };
        $.ajax({
            type: "POST",
            url: "/create_scirpt",
            data: data,
            success:function(){
                window.location.reload();
            }
        });


    });


    $(".tbody").on("click",'button',function(){
        var tem=this.className;
        var bu = $(this).val();
        if(bu=="修改"){
            $("."+tem).empty();
            $(this).val("提交");
            $("."+tem).append("提交");
            $('.'+tem+"_script_content_n").removeAttr("disabled");
            $('.'+tem+"_script_content_o").removeAttr("disabled");
            $('.'+tem+"_name").removeAttr("disabled");
        }
        else{
            var script_info = $('.'+tem+"_name").val();
            var script_content_n = $('.'+tem+"_script_content_n").val();
            var script_content_o = $('.'+tem+"_script_content_o").val();
            var data=
                    {
                        "script_name": tem,
                        "script_info": script_info,
                        "script_content_o": script_content_o,
                        "script_content_n": script_content_n
                    };
            $.ajax({
            type: "POST",
            url: "/edit_scirpt",
            data: data,
            success:function(){
                window.location.reload();
            }
        });

        }
    });

});

