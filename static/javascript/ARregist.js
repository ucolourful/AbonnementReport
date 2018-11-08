//AR 注册页 JS
layui.use(['element', 'form'], function () {
    var element = layui.element;
    var form = layui.form;

    //自定义验证规则
    form.verify({
        title: function (value) {
            if (value.length < 5) {
                return '标题也太短了吧';
            }
        }
        , pass: [/(.+){6,12}$/, '密码必须6到12位']
    });

    //初始赋值
    // form.val('first', {
    //     'username': '测试11111'
    //     , 'password': 123123
    //     , 'password2': 123123
    //     , 'email': 'xu@sentsin.com'
    //     , 'productline': '虚拟存储VS'
    // });

    form.on('select(interest)', function (data) {
        console.log('select.interest: ', this, data);
    });
    //监听提交
    form.on('submit(*)', function (data) {
        console.log(data);
        alert(JSON.stringify(data.field));
        // return false;
    });
});