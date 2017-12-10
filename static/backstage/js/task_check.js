layui.use(['layer', 'form', 'table', 'laydate', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        laytpl = layui.laytpl,
        laydate = layui.laydate,
        common = layui.common;

    //取url里面的参数
    $(function () {
        (function ($) {
            $.getUrlParam = function (name) {
                var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
                var r = window.location.search.substr(1).match(reg);
                if (r != null) return unescape(r[2]);
                return null;
            }
        })($);
    });

    var list_id = $.getUrlParam('list_id');

    var data_init = null;
    $(function () {
        $.ajax({
            url: '/v1/task/check/?list_id=' + list_id,
            async: false,
            success: function (data) {
                if (data.status == 0) {
                    layer.msg(data.msg, {icon: 1, time: 1000});
                    layer.closeAll('page');
                    data_init = data.data;
                    setTimeout(function () {
                    }, 1000);
                } else {
                    layer.msg(data.msg, {icon: 2, time: 1000});
                }
            },
            error: function (data) {
                layer.msg('获取数据失败', {icon: 2, time: 1000});
            },
        });
        return false;
    });

    var getTpl = task.innerHTML,
        view = document.getElementById('view');
    laytpl(getTpl).render(data_init, function (html) {
        view.innerHTML = html;
    });


    $('#larry_group .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });

    laydate.render({
        elem: '#date1',
        type: 'datetime',
        value: data_init.stime
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