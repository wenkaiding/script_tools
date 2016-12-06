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
        var status = this.className+"_status";
        if (this.value=="Intranet"||this.value=="Outside"){
            $('#loading').fadeIn('fast');
            var data={env:this.value,fp:$('.fp_sel').val(),scrip_name:name};
            //Ajax调用处理
            $.ajax({
                type: "POST",
                url: "/run_scrip",
            });
            $.ajax({
                type: "POST",
                url: "/get_script_status",
                data: data,
                 success:function(result){
                     $(this.ClassName)
                 }
            });
        }
        else{
            var data={env:this.value,fp:$('.fp_sel').val(),scrip_name:name};
            //Ajax调用处理
            $.ajax({
                type: "POST",
                url: "/get_results",
                data: data,
                 success:function(result){
                     alert(result)
                 }
            });
        }

    });
});

