layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        common = layui.common;

    var tableIns = table.render({
        elem: '#tempTables',
        cols: [
            [{
                field: 'temp_id', width: 50, title: 'ID', sort: true,
            }, {
                field: '', width: 120, title: '模板名称', toolbar: '#tempnamebar'
            }, {
                title: '删除', width: 80, align: 'center', toolbar: '#tempbar', fixed: "right"
            }]

        ],
        url: '/v1/task/temp/',
        page: false,
        even: true,
        height: 'full-150',
        id: 'tempTables',
    });

    table.on('tool(tempTables)', function (obj) {
        var data = obj.data;
        if (obj.event === "temp_name") {
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
                        field: 'command', width: 220, title: '命令', align: 'center'
                    }, {
                        field: 'forc_ip', width: 100, title: '指定主机', align: 'center'
                    }, {
                        field: 'exec_user', width: 100, title: '执行用户', align: 'center', edit: 'text'
                    }, {
                        field: 'trigger', width: 80, title: '触发', align: 'center', edit: 'text'
                    }, {
                        title: '删除', width: 120, align: 'center', toolbar: '#cmdbar', fixed: "right"
                    }]

                ],
                url: "/v1/task/details/?temp_id=" + obj.data.temp_id,
                page: false,
                even: true,
                height: 'full-150',
                id: 'cmdTables',
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
                    type: 'PATCH',
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
                var IdArr = [];
                IdArr.push(data.cmd_id);
                $.ajax({
                    url: "/v1/task/cmd/",
                    type: 'DELETE',
                    data: JSON.stringify({"cmd_id": IdArr}),
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
        del: function () {
            var checkStatus = table.checkStatus('cmdTables'),
                data = checkStatus.data;
            var IdArr = [];
            layui.each(data, function (idx, obj) {
                IdArr.push(obj.cmd_id);
            });
            layer.confirm('确定删除？', function (index) {
                console.log(data)
                $.ajax({
                    url: "/v1/task/cmd/",
                    type: 'DELETE',
                    data: JSON.stringify({"cmd_id": IdArr}),
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
                                });
                            }, 1000);
                        } else {
                            layer.msg(data.msg, {icon: 2, time: 1000});
                        }
                    },
                    error: function () {
                        layer.msg('删除失败', {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
            });
        }
    };
});