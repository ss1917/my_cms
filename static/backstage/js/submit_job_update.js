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

    //监听表格复选框选择
    table.on('checkbox(cmdTables)', function (obj) {
        console.log(obj)
    });


    var layer = parent.layer === undefined ? layui.layer : parent.layer;
    form.render();


    laydate.render({
        elem: '#date1',
        type: 'datetime',
        min: 0,
        value: '2038-01-01 14:00:00',
    });

    form.on('submit(submit)', function (data) {
        $.ajax({
            url: "/v1/jobs/update/",
            type: 'POST',
            data: JSON.stringify(data.field),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                if (data.status == 0) {
                    layer.msg(data.msg, {icon: 1, time: 1000});
                    layer.closeAll('page');
                    setTimeout(function () {
                    }, 1000);
                } else {
                    layer.msg(data.msg, {icon: 2, time: 1000});
                }

            },
            error: function (data) {
                layer.msg('提交任务失败', {icon: 2, time: 1000});
            },
        });
        return false;
    });
});