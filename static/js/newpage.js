/**
 *  * Created by dingwenkai on 16/10/11.
 *   */
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
        var script_info = $('.'+tem+"_name").html();
        var script_content_n = $('.'+tem+"_script_content_n").html();
        var script_content_o = $('.'+tem+"_script_content_o").html();
        script_content_n = script_content_n.replace(/'/g, "&#39;");
        script_content_o = script_content_o.replace(/'/g, "&#39;");
        var bu = $(this).val();
        if(bu=="修改"){
            $("."+tem).empty();
            $(this).val("提交");
            $("."+tem).append("提交");
            $('.'+tem+"_name").empty();
            $('.'+tem+"_script_content_n").empty();
            $('.'+tem+"_script_content_o").empty();
            $('.'+tem+"_name").html("<input class='"+tem+"_name' type='text' style='width:100%' value='"+script_info+"'>");
            $('.'+tem+"_script_content_n").html("<input class='"+tem+"_script_content_n' type='text' style='width:100%' value='"+script_content_n+"'>");
            $('.'+tem+"_script_content_o").html("<input class='"+tem+"_script_content_o' type='text' style='width:100%' value='"+script_content_o+"'>");
        }
        else{
            var script_info = $("td ."+tem+"_name").val();
            var script_content_n = $("td ."+tem+"_script_content_n").val();
            var script_content_o = $("td ."+tem+"_script_content_o").val();
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
            success:function(hnit){
                alert(hnit);
                window.location.reload();
            }
        });

        }
    });
    $('#search').keydown(function(e){
        if(e.keyCode==13){
            var page = "edit_page";
            var name = $(this).val();
            var data = {page:page,name:name};
            $(".tbody").empty();
            $.ajax({
                type: "POST",
                url: "/search",
                data: data,
                success:function(result){
                    $(".tbody").empty();
                    $(".tbody").append(result)

                }
            });

        }
    });

});


