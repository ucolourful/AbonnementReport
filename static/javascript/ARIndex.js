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

    $('#viewAllUser').on('click',function(){
    	layer.msg("viewAllUser");
    });

    $('.layui-btn1').on('click',function(){
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
					})
				}
			)
    	}else{
    		// TODO，这里可以优化一下，先通过value判定confirm的str
			if (this.value == "0"){
				if ( confirm("请确认是否取消订阅此版本邮件？") == true){
					$.post("/abonnementReport",{'versionID':versionID,'doAction':event.value},function(ret){
					location.reload()
					})
					return
				}
				return
			}
    	}
    });

    $('.layui-btn2').on('click',function(){
    	if (this.id === "viewAllUser") { return };
    	layer.alert(this.id)
    });
});

//// 订阅版本
//function abonnementReport(event){
//    // 获取versionID
//    versionID = event.name.split("_")[1]
//
//    // 已订阅,这里处理"取消订阅"的功能
//    if (event.value == "0"){
//        if ( confirm("请确认是否取消订阅此版本邮件？") == true){
//            $.post("/abonnementReport",{'versionID':versionID,'doAction':event.value},function(ret){
//                location.reload()
//            })
//            return
//        }
//        return
//    }
//    // 未订阅,这里处理"订阅报告"的功能
//
//    if (event.value == "1"){
//        if ( confirm("请确认是否订阅此版本邮件？") == true){
//            $.post("/abonnementReport",{'versionID':versionID,'doAction':event.value},function(ret){
//                location.reload()
//            })
//            return
//        }
//        return
//    }
//}
//
//// 查看订阅人
//function viewVersionUsers(event){
//    // 获取版本名称
//    versionName = event.name
//
//    // 新开标签页查看版本订阅人
//    if ( versionName != "" ){
//        window.open("/viewVersionUsers?versionName="+versionName,"viewVersionUsers","menubar=0,scrollbars=1, resizable=1,status=1,titlebar=0,toolbar=0,location=1")
//    } else {
//        window.open("/viewVersionUsers","viewVersionUsers","menubar=0,scrollbars=1, resizable=1,status=1,titlebar=0,toolbar=0,location=1")
//    }
//}
