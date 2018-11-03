// 添加版本
function addVersion(){
    userAuth = document.getElementById("userAuth").value;
    if ( userAuth == "admin" ) {
        var versionName = document.getElementById("versionName").value;
        if ( versionName == "" ) {
            alert("请输入版本号进行添加！！！")
            return
        }
        $.post("/addVersion",{'versionName':versionName},function(ret){
            location.reload()
        })
    }
    else {
        alert("您没有添加版本的权限！！！");
        return
    }
}

// 删除版本
function delVersion(event){
    userAuth = document.getElementById("userAuth").value;
    if ( userAuth == "admin" ) {
        var versionID = event.name.split("_")[1]
        $.post("/delVersion",{'versionID':versionID},function(ret){
            location.reload()
        })
    }
    else {
        alert("您没有删除版本的权限！！！");
        return
    }
}
