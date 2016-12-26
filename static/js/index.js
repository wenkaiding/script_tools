/**
 * Created by dingwenkai on 16/10/11.
 */
$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/get_table_info",
        success:function(html){
            $(".tbody").empty();
            $(".tbody").append(html)
        }
    });
    $(".tbody").on("click",'button',function(){
        var name = this.className;
        var status = "."+this.className+"_status";

        if (this.value=="Intranet"||this.value=="Outside"){
            $(status).empty();
            $(status).append("执行中");
            $('#loading').fadeIn('fast');
            var data={env:this.value,fp:$('.fp_sel').val(),scrip_name:name};
            //Ajax调用处理
            $.ajax({
                type: "POST",
                url: "/run_scrip",
                data: data
            });
            $.ajax({
                type: "POST",
                url: "/get_script_status",
                data: data,
                success:function(result){
                     $(status).empty();
                     $(status).append(result)

                }
            });
        }
        else{
            var data={env:this.value,fp:$('.fp_sel').val(),script_name:name};
            //Ajax调用处理
            $.ajax({
                type: "POST",
                url: "/get_result_page",
                data: data,
                success:function(result){
                    $('.sripts_result').empty();
                    $('.sripts_result').append(result)

                }
            });
        }

    });

    $('#search').keydown(function(e){
        if(e.keyCode==13){
            var page = "php_page";
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

