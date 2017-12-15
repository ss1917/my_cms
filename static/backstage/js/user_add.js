layui.use(['jquery', 'layer', 'form', 'upload'], function () {
    var $ = layui.$,
        layer = layui.layer,
        upload = layui.upload,
        form = layui.form;


    var uploadInst = upload.render({
        elem: '#larry_photo' //绑定元素
        ,
        url: '/upload/' //上传接口
        ,
        done: function (res) {
            //上传完毕回调
        },
        error: function () {
            //请求异常回调
        }
    });


    form.on('submit(submit)', function (data) {
        var index = parent.layer.getFrameIndex(window.name);
        $.ajax({
            url: "/v1/accounts/user/",
            type: 'POST',
            data: JSON.stringify(data.field),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            //async:false,
            success: function (data) {
                console.log(data.status);
                if (data.status == 0) {
                    layer.msg(data.msg, {icon: 1, time: 1000});
                    layer.closeAll('page');
                    setTimeout(function () {
                        //window.location.href = '/';
                        location.reload();
                        parent.layer.close(index);
                    }, 1000);
                } else {
                    layer.msg(data.msg, {icon: 2, time: 1000});
                }

            },
            error: function (data) {
                layer.msg('注册失败', {icon: 2, time: 1000});
            },

        });
        return false;
    });
});