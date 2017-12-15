layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        common = layui.common;

    var tableIns = table.render({
        elem: '#argsTables',
        cols: [
            [{
                checkbox: true, width: 80, fixed: true
            }, {
                field: 'args_id', width: 80, title: 'ID', sort: true,
                // fixed: true
            }, {
                field: 'args_name', width: 200, title: '名称', align: 'center'
            }, {
                field: 'args_self', width: 250, title: '参数', align: 'center', edit: 'text'
            }, {
                field: 'creator', width: 100, title: '创建人', align: 'center'
            }, {
                field: 'utime', width: 180, title: '修改时间', align: 'center'
            }, {
                title: '常用操作', width: 120, align: 'center', toolbar: '#args_bar', fixed: "right"
            }]

        ],
        url: '/v1/task/args/',
        page: true,
        even: true,
        height: 'full-150',
        id: 'argsTables',
        limit: 20,
    });

    //监听表格复选框选择
    table.on('checkbox(argsTables)', function (obj) {
        console.log(obj)
    });


    //监听工具条
    table.on('tool(argsTables)', function (obj) {
        var data = obj.data;
        if (obj.event === 'edit') {
            layer.confirm('确定要保存编辑吗？：' + data.args_name, function (index) {
                $.ajax({
                    url: "/v1/task/args/",
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
                IdArr.push(data.args_id);
                $.ajax({
                    url: "/v1/task/args/",
                    type: 'DELETE',
                    data: JSON.stringify({"args_id": IdArr}),
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
                content: '/static/backstage/templates/task/args_add.html',
                area: ['320px', '195px'],
                anim: 1,
                title: '新建参数',
                maxmin: true,
                end: function () {
                    table.reload('argsTables')
                }
            });
            layer.full(index);
        },
        search: function () {
            var name_search = $('#name_search');
            //执行重载
            table.reload('argsTables', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    args_name: name_search.val()
                }
            });
        },
        del: function () {
            var checkStatus = table.checkStatus('argsTables'),
                data = checkStatus.data;
            var IdArr = [];
            layui.each(data, function (idx, obj) {
                IdArr.push(obj.args_id);
            });
            layer.confirm('确定删除？', function (index) {
                console.log(data)
                $.ajax({
                    url: "/v1/task/args/",
                    type: 'DELETE',
                    data: JSON.stringify({"args_id": IdArr}),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                table.reload('argsTables', {
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