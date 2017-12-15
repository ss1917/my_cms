layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        common = layui.common;

    var tableIns = table.render({
        elem: '#cmdTables',
        cols: [
            [{
                checkbox: true, width: 60, fixed: true
            }, {
                field: 'cmd_id', width: 60, title: 'ID', sort: true,
                // fixed: true
            }, {
                field: 'cmd_name', width: 120, title: '名称', align: 'center'
            }, {
                field: 'command', width: 250, title: '命令', align: 'center'
            }, {
                field: 'args', width: 300, title: '参数', align: 'center', edit: 'text'
            }, {
                field: 'forc_ip', width: 120, title: '指定主机', align: 'center', edit: 'text'
            }, {
                field: 'creator', width: 100, title: '创建人', align: 'center'
            }, {
                field: 'ctime', width: 180, title: '创建时间', align: 'center'
            }, {
                field: 'utime', width: 180, title: '修改时间', align: 'center'
            }, {
                title: '常用操作', width: 120, align: 'center', toolbar: '#cmdbar', fixed: "right"
            }]

        ],
        url: '/v1/task/cmd/',
        page: true,
        even: true,
        height: 'full-150',
        id: 'cmdTables',
        limit: 20,
    });

    //监听表格复选框选择
    table.on('checkbox(cmdTables)', function (obj) {
        console.log(obj)
    });


    //监听工具条
    table.on('tool(cmdTables)', function (obj) {
        var data = obj.data;
        if (obj.event === 'edit') {
            layer.confirm('确定要保存编辑吗？：' + data.cmd_name, function (index) {
                $.ajax({
                    url: "/v1/task/cmd/",
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
            var index = layer.open({
                type: 2,
                content: '/static/backstage/templates/task/cmd_add.html',
                area: ['320px', '195px'],
                maxmin: true,
                end: function () {
                    table.reload('cmdTables')
                }
            });
            layer.full(index);
        },
        search: function () {
            var name_search = $('#name_search');
            //执行重载
            table.reload('cmdTables', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    cmd_name: name_search.val()
                }
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