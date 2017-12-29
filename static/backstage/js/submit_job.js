layui.use(['layer', 'form', 'table', 'laydate', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        laytpl = layui.laytpl,
        laydate = layui.laydate,
        common = layui.common;

    $('#larry_group .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });


    var layer = parent.layer === undefined ? layui.layer : parent.layer;
    $("select[name=aaa]").val(["4"]);
    form.render();


    laydate.render({
        elem: '#date1',
        type: 'datetime',
        value: '2038-01-01 14:00:00',
    });

    form.on('submit(submit)', function (data) {
        $.ajax({
            url: "/v1/task/list/",
            type: 'PUT',
            //data: JSON.stringify(data.field),
            data: JSON.stringify({
                "start_time": data.field.start_time,
                "list_handle": "list_start",
                "list_id": data_init.list_id
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                console.log(data.status);
                if (data.status == 0) {
                    layer.msg(data.msg, {icon: 1, time: 1000});
                    layer.closeAll('page');
                    setTimeout(function () {
                        window.history.go(-1)
                    }, 1000);
                } else {
                    layer.msg(data.msg, {icon: 2, time: 1000});
                }

            },
            error: function (data) {
                layer.msg('失败', {icon: 2, time: 1000});
            },

        });
        return false;
    });
});