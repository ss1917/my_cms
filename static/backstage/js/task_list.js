layui.use(['layer', 'form', 'table', 'common', 'element',], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        common = layui.common,
        element = layui.element;

    //table.init('filter', options);
    var tableIns = table.render({
        elem: '#tasklistTables',
        cols: [
            [{
                field: 'list_id', width: 60, title: 'ID', sort: true,
                // fixed: true
            }, {
                field: 'task_name', width: 150, title: '任务名称', align: 'center', templet: '#checkTpl'
            }, {
                field: 'task_type', width: 100, title: '任务类型', align: 'center',
            }, {
                field: 'creator', width: 100, title: '提交人', align: 'center',
            }, {
                field: 'executor', width: 100, title: '接手人', align: 'center',
            }, {
                title: '常用操作', width: 120, align: 'center', toolbar: '#taskbar'
            }, {
                field: 'status', width: 80, title: '状态', align: 'center', templet: '#statusTpl', unresize: true,
            }, {
                field: 'ctime', width: 180, title: '创建时间', align: 'center',
            }, {
                field: 'stime', width: 180, title: '开始时间', align: 'center',
            }, {
                title: '任务详情', width: 120, align: 'center', toolbar: '#publishbar', fixed: "right"
            }]
        ],
        url: '/v1/task/list/',
        page: true,
        even: true,
        height: 'full-150',
        id: 'tasklistTables',
        limit: 20,
    });

    var tableIns = table.render({
        elem: '#histTables',
        cols: [
            [{
                field: 'list_id', width: 60, title: 'ID', sort: true,
                // fixed: true
            }, {
                field: 'task_name', width: 150, title: '任务名称', align: 'center', templet: '#checkTpl'
            }, {
                field: 'task_type', width: 100, title: '任务类型', align: 'center'
            }, {
                field: 'creator', width: 80, title: '提交人', align: 'center'
            }, {
                field: 'executor', width: 80, title: '接手人', align: 'center'
            }, {
                field: 'schedule', width: 80, title: '进度', align: 'center', templet: '#scheduleTpl', unresize: true,
            }, {
                field: 'ctime', width: 180, title: '创建时间', align: 'center'
            }, {
                field: 'stime', width: 180, title: '开始时间', align: 'center'
            }, {
                title: '任务详情', width: 180, align: 'center', toolbar: '#publishbar', fixed: "right"
            }]

        ],
        url: '/v1/task/list/?history=history',
        page: true,
        even: true,
        //height: 'full-150',
        id: 'histTables',
        limit: 20,
    });

    /*
    $("[name=publishTables]").click(function () {
        table.reload("publishTables");
    });
    $("[name=histTables]").click(function () {
        table.reload("histTables");
    });
    */

    //监听工具条
    table.on('tool(tasklistTables)', function (obj) {
        var data = obj.data;
        if (obj.event === 'take_over') {
            layer.confirm('确定要释放此任务？？？', function (index) {
                $.ajax({
                    url: "/v1/task/list/",
                    type: 'PUT',
                    data: JSON.stringify({"list_id": data.list_id, "list_handle": "take_over"}),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                table.reload('tasklistTables', {
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                });
                            }, 1000);
                        } else {
                            layer.msg(data.msg, {icon: 2, time: 1000});
                        }
                    },
                    error: function (data) {
                        layer.msg('接手失败', {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
            });

        } else if (obj.event === 'task_release') {
            layer.confirm('确定要释放此任务？？？', function (index) {
                $.ajax({
                    url: "/v1/task/list/",
                    type: 'PUT',
                    data: JSON.stringify({"list_id": data.list_id, "list_handle": "task_release"}),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                table.reload('tasklistTables', {
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                });
                            }, 1000);
                        } else {
                            layer.msg(data.msg, {icon: 2, time: 1000});
                        }
                    },
                    error: function (data) {
                        layer.msg('释放失败', {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
            });

        } else if (obj.event === 'list_stop') {
            layer.confirm('确定要终止当前任务吗?', function (index) {
                $.ajax({
                    url: "/v1/task/list/",
                    type: 'PUT',
                    data: JSON.stringify({"list_id": data.list_id, "list_handle": "list_stop"}),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                table.reload('tasklistTables', {
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                });
                            }, 1000);
                        } else {
                            layer.msg(data.msg, {icon: 2, time: 1000});
                        }
                    },
                    error: function (data) {
                        layer.msg('失败', {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
            });

        }
    });

});