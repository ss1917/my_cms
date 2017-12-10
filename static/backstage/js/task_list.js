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
                field: 'task_name', width: 150, title: '任务名称', align: 'center',templet: '#checkTpl'
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
        height: 'full-200',
        id: 'tasklistTables',
        limit: 10,
    });

    var tableIns2 = table.render({
        elem: '#histTables',
        cols: [
            [{
                field: 'list_id', width: 60, title: 'ID', sort: true,
                // fixed: true
            }, {
                field: 'task_name', width: 150, title: '任务名称', align: 'center',templet: '#checkTpl'
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
        id: 'histTables',
        limit: 30,
    });


    $("[name=publishTables]").click(function () {
        table.reload("publishTables");
    });
    $("[name=histTables]").click(function () {
        table.reload("histTables");
    });


    //监听工具条
    table.on('tool(tasklistTables)', function (obj) {
        var data = obj.data;
        //console.log(data);
        if (obj.event === 'check1') {
            layer.confirm('确定要保存编辑吗？：' + data.username, function (index) {
                $.ajax({
                    url: "/v1/accounts/user/",
                    type: 'PUT',
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                //window.location.href = '/';
                            }, 1000);
                        } else {
                            layer.msg(data.msg, {icon: 2, time: 1000});
                        }
                    },
                    error: function (data) {
                        layer.msg(data.msg, {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
                return false;
            });
        } else if (obj.event === 'xiangqing') {
            console.log(data.list_id);
            var index = layer.open({
                type: 2,
                content: ['/static/backstage/templates/task/task_details.html?list_id=' + data.list_id],
                area: ['320px', '195px'],
                maxmin: true,
                success: function (index, layero) {//回调
                    var list_id = data.list_id
                },
                end: function (index) {
                    layer.close(index);
                },

            });
            layer.full(index);

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

    $('#larry_group .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });

    var active = {
        add: function () {
            var index = layer.open({
                type: 2,
                content: '/static/backstage/html/user_manage/user_add.html',
                area: ['320px', '195px'],
                maxmin: true
            });
            layer.full(index);
        },
    };
});