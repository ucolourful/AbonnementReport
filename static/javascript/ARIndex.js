// 首页JS
layui.use(['element','layer','jquery'], function () {
    var element = layui.element;
    layer = layui.layer;
    $ = layui.jquery;

    $('#addversion').on('click',function(){
    	if ($('#userAuth').val() ===  "admin") {
    		if ($('#inputVersion').val() === "") {
    			layer.alert("请输入版本号进行添加！")
    		}else{
				$.post("/addVersion",{'versionName':$('#inputVersion').val()},function(ret){
				   if (ret.status === 0){
				   		layer.msg(ret.msg);
				   		setTimeout("location.reload()", 1000);
				   }
				   if (ret.status === 1) {
				   		layer.alert(ret.msg);
				   }
				})
    		}
    	} else{
    		layer.msg("您没有添加版本的权限！！！");
    	}
    	return
    });

    $('.layui-btn-opt').on('click',function(){
    	if (this.id === "addversion") { return };
    	var versionID = this.name.split("_")[1];
    	if ($('#userAuth').val() === "admin") {
    		layer.confirm("请确认是否删除此版本？",{
    			time:0,
    			btn:['确认','取消']},
    			function(){
    				$.post("/delVersion",{'versionID':versionID},function(ret){
						if (ret.status === 0){
							layer.msg(ret.msg);
							setTimeout("location.reload()", 1000);
						}
						if (ret.status === 1) {
							layer.alert(ret.msg);
						}
					});
				}
			);
    	}else{
    	    var tmp = this.value
    	    if (tmp === "0"){
                str = "请确认是否取消订阅此版本邮件？"
    	    };
    	    if (tmp === "1"){
                str = "请确认是否订阅此版本邮件？"
    	    };
            layer.confirm(str,{
                time:0,
                btn:['确认','取消']},
                function(){
                    $.post("/abonnementReport",{'versionID':versionID,'doAction':tmp},function(ret){
                        if (ret.status === 0){
                            layer.msg(ret.msg);
                            setTimeout("location.reload()", 1000);
                        }
                        if (ret.status === 1) {
                            layer.alert(ret.msg);
                        }
                    })
                }
            );
    	}
    });

    $('.layui-btn-view').on('click',function(){
    	versionName = this.name
    	if ( versionName === "" ){
    	    url = "/viewVersionUsers"
    	} else {
    	    url = "/viewVersionUsers?versionName="+versionName
    	}
    	$.get(url,function(ret){
    	    layer.alert(JSON.stringify(ret.msg));
    	});
    });
});
