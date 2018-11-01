
// 搜索特定人的订阅情况
function mySearch() {
    personName = document.getElementById("personName").value;
    if ( personName == "" ) {
        alert("请输入工号进行查询！！！");
    }
    else {
        alert(personName);
    }
}

// 添加版本
function myAddVersion(){
    username = document.getElementById("username").innerText;
    if ( username == "admin" ) {
        var versionName = document.getElementById("personName").value;
        if ( versionName == "" ) {
            alert("请输入版本号进行添加！！！")
            return
        }
        $.get("/addVersion",{'versionName':versionName},function(ret){
            location.reload()
        })
    }
    else {
        alert("您没有添加版本的权限！！！");
    }
}

// 删除版本
function myDelVersion(event){
    username = document.getElementById("username").innerText;
    if ( username == "admin" ) {
        var versionID = event.id
        $.get("/delVersion",{'versionID':versionID},function(ret){
            location.reload()
        })
    }
    else {
        alert("您没有删除版本的权限！！！");
    }
}
