layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        laytpl = layui.laytpl,
        common = layui.common;

    var data_init = null;
    var temp_id = null
    $(function () {
        $.ajax({
            url: '/v1/task/cmd/',
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

    var tableIns = table.render({
        elem: '#tempTables',
        cols: [
            [{
                field: 'temp_id', width: 50, title: 'ID', sort: true,
            }, {
                field: '', width: 110, title: '模板名称', toolbar: '#tempnamebar'
            }, {
                title: '删除', width: 60, align: 'center', toolbar: '#tempbar', fixed: "right"
            }]

        ],
        url: '/v1/task/temp/',
        page: false,
        even: true,
        height: 'full-150',
        id: 'tempTables',
    });

    var tableIns = table.render({
        elem: '#cmdTables',
        cols: [
            [{
                field: 'group', width: 60, title: '组', sort: true, edit: 'text'
            }, {
                field: 'level', width: 80, title: '优先级', edit: 'text'
            }, {
                field: 'cmd_name', width: 120, title: '名称', align: 'center'
            }, {
                field: 'command', width: 200, title: '命令', align: 'center'
            }, {
                field: 'exec_user', width: 100, title: '执行用户', align: 'center', edit: 'text'
            }, {
                field: 'trigger', width: 80, title: '触发', align: 'center', edit: 'text'
            }, {
                field: 'args', width: 220, title: '参数', align: 'center', edit: 'text'
            }, {
                field: 'forc_ip', width: 100, title: '指定主机', align: 'center'
            }, {
                title: '操作', width: 120, align: 'center', toolbar: '#cmdbar', fixed: "right"
            }]

        ],
        url: "/v1/task/details/" ,
        page: false,
        even: true,
        height: 'full-150',
        id: 'cmdTables',
    });

    table.on('tool(tempTables)', function (obj) {
        var data = obj.data;
        temp_id = obj.data.temp_id
        if (obj.event === "temp_name") {
            table.reload('cmdTables', {
                url: "/v1/task/details/?temp_id=" + obj.data.temp_id,
            });

        } else if (obj.event === 'del') {
            layer.confirm('确定删除此模板？？ 删除后无法恢复！！！', function (index) {
                $.ajax({
                    url: "/v1/task/temp/",
                    type: 'DELETE',
                    data: JSON.stringify({"temp_id": data.temp_id}),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                obj.del();
                            }, 1000);
                        } else {
                            layer.msg(data.msg, {icon: 2, time: 1000});
                        }
                    },
                    error: function () {
                        layer.msg('失败', {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
            });
        }
    });

    //监听工具条
    table.on('tool(cmdTables)', function (obj) {
        var data = obj.data;
        if (obj.event === 'edit') {
            layer.confirm('确定要保存编辑吗？：' + data.cmd_name, function (index) {
                $.ajax({
                    url: "/v1/task/details/",
                    type: 'PUT',
                    data: JSON.stringify(data),
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
                    error: function () {
                        layer.msg('错误', {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
                return false;
            });
        } else if (obj.event === 'del') {
            layer.confirm('删除行?', function (index) {
                $.ajax({
                    url: "/v1/task/details/",
                    type: 'DELETE',
                    data: JSON.stringify({"id": data.id}),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                obj.del();
                            }, 1000);
                        } else {
                            layer.msg(data.msg, {icon: 2, time: 1000});
                        }
                    },
                    error: function () {
                        layer.msg('失败', {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
            });

        }
    });

    $('#larry_group .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });

    var active = {
        add: function () {
            var temp_name = $('#temp_name');
            console.log(temp_name.val())
            $.ajax({
                url: "/v1/task/temp/",
                type: 'POST',
                data: JSON.stringify({"temp_name": temp_name.val()}),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data) {
                    if (data.status == 0) {
                        layer.msg(data.msg, {icon: 1, time: 1000});
                        layer.closeAll('page');
                        setTimeout(function () {
                            parent.location.reload();
                        }, 1000);
                    } else {
                        layer.msg(data.msg, {icon: 2, time: 1000});
                    }
                },
                error: function () {
                    layer.msg('添加模板失败', {icon: 2, time: 1000});
                    return false;
                },
            });
        },
        add1: function () {
            var cmd_id = $('#cmd_id');
            $.ajax({
                url: "/v1/task/details/",
                type: 'PATCH',
                data: JSON.stringify({"cmd_id": cmd_id.val(), 'temp_id': temp_id}),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data) {
                    if (data.status == 0) {
                        layer.msg(data.msg, {icon: 1, time: 1000});
                        layer.closeAll('page');
                        setTimeout(function () {
                            table.reload('cmdTables', {
                                page: {
                                    curr: 1 //重新从第 1 页开始
                                }
                                , where: {
                                    temp_id: temp_id
                                }
                            });
                        }, 1000);
                    } else {
                        layer.msg(data.msg, {icon: 2, time: 1000});
                    }
                },
                error: function () {
                    layer.msg('添加模板失败', {icon: 2, time: 1000});
                    return false;
                },
            });
        }
    };
});