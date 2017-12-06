layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        laytpl = layui.laytpl,
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
    var task_group = $.getUrlParam('task_group');
    var task_level = $.getUrlParam('task_level');
    var exec_ip = $.getUrlParam('exec_ip');
    var data_init = null;
    $(function () {
        $.ajax({
            url: '/v1/task/log/?list_id=' + list_id + '&exec_ip=' + exec_ip + '&task_group=' + task_group + '&task_level=' + task_level,
            async: false,
            success: function (data) {
                if (data.code == 0) {
                    layer.msg(data.msg, {icon: 1, time: 1000});
                    layer.closeAll('page');
                    data_init = data;
                    setTimeout(function () {
                    }, 1000);
                } else {
                    layer.msg(data.msg, {icon: 2, time: 1000});
                }
            },
            error: function (data) {
                layer.msg(data.msg, {icon: 2, time: 1000});
            },
        });
        return false;
    });

    var getTpl = log.innerHTML,
        view = document.getElementById('view');
    laytpl(getTpl).render(data_init, function (html) {
        view.innerHTML = html;
    });
});