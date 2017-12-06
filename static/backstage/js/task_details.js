layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
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

    var data_init = null;
    $(function () {
        $.ajax({
            url: '/v1/task/sched/?list_id=' + list_id,
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

    var getTpl = task.innerHTML,
        view = document.getElementById('view');
    laytpl(getTpl).render(data_init, function (html) {
        view.innerHTML = html;
    });

    var tableIns = table.render({
        elem: '#taskdetailsTables',
        cols: [
            [{
                field: '', width: 60, title: '', sort: true,
            }, {
                field: 'exec_ip', width: 120, title: '执行主机', align: 'center',
            }, {
                field: 'task_group', width: 80, title: '执行组', align: 'center',
            }, {
                field: 'task_level', width: 80, title: '优先级', align: 'center',
            }, {
                field: 'task_name', width: 150, title: '任务名称', align: 'center',
            }, {
                field: 'task_cmd', width: 200, title: '任务命令', align: 'center',
            }, {
                field: 'task_status', width: 100, title: '状态', align: 'center', templet: '#statusTpl', unresize: true,
            }, {
                title: '操作', width: 220, align: 'center', toolbar: '#publishbar', fixed: "right"
            }]
        ],
        url: '/v1/task/sched/?list_id=' + list_id,
        even: true,
        page: false,
        id: 'taskdetailsTables',
    });


    //监听表格复选框选择
    table.on('checkbox(taskdetailsTables)', function (obj) {
        console.log(obj)
    });

    //监听开关
    form.on('switch(sexDemo)', function (obj) {
        var data = obj.data;
        //layer.tips(this.value + this.name + '：' + obj.elem.checked, obj.othis);
        $.ajax({
            url: "/v1/accounts/user/",
            type: 'PATCH',
            data: JSON.stringify({"user_id": this.value}),
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
                layer.msg('失败', {icon: 2, time: 1000});
            },
        });
        return false;

    });

    //监听工具条
    table.on('tool(taskdetailsTables)', function (obj) {
        var data = obj.data;
        if (obj.event === 'hand') {
            layer.confirm('确定要手动执行吗？？？', function (index) {
                $.ajax({
                    url: "/v1/task/sched/",
                    type: 'PUT',
                    data: JSON.stringify({
                        "list_id": list_id,
                        "sched_id": data.sched_id,
                        "task_handle": "hand"
                    }),
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
                        layer.msg(data.msg, {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
                return false;
            });
        } else if (obj.event === 'redo') {
            layer.confirm('重做？？？', function (index) {
                $.ajax({
                    url: "/v1/task/sched/",
                    type: 'PUT',
                    data: JSON.stringify({
                        "list_id": list_id,
                        "sched_id": data.sched_id,
                        "task_handle": "redo"
                    }),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                table.reload('taskdetailsTables', {
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                    , where: {
                                        task_group: data.task_group,
                                        exec_ip: data.exec_ip
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
        } else if (obj.event === 'task_log') {
            console.log(data.list_id, data.exec_ip, data.task_group, data.task_level)
            var index = layer.open({
                type: 2,
                content: '/static/backstage/templates/publish_code/task_log.html?list_id=' + data.list_id + '&exec_ip=' + data.exec_ip+'&task_group='+data.task_group+'&task_level='+data.task_level,
                area: ['320px', '195px'],
                maxmin: true
            });
            layer.full(index);

        } else if (obj.event === 'stop') {
            layer.confirm('终止当前组任务？？？', function (index) {
                $.ajax({
                    url: "/v1/task/sched/",
                    type: 'PUT',
                    data: JSON.stringify({
                        "list_id": list_id,
                        "sched_id": data.sched_id,
                        "task_handle": "stop"
                    }),
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
        search: function () {
            var input_value = [];
            $(this).siblings().each(function (index, item) {
                input_value.push($(item).val());
            });

            var group_search = input_value[0];
            var hosts_search = input_value[1];
            //执行重载
            table.reload('taskdetailsTables', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    task_group: group_search,
                    exec_ip: hosts_search,
                }
            });
        },
        del: function () {
            var checkStatus = table.checkStatus('userTables'),
                data = checkStatus.data;
            var IdArr = [];
            layui.each(data, function (idx, obj) {
                IdArr.push(obj.user_id);
            });
            layer.confirm('确定删除？', function (index) {
                console.log(data)
                $.ajax({
                    url: "/v1/accounts/user/",
                    type: 'DELETE',
                    data: JSON.stringify({"user_id": IdArr}),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 0) {
                            layer.msg(data.msg, {icon: 1, time: 1000});
                            layer.closeAll('page');
                            setTimeout(function () {
                                table.reload('userTables', {
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                });
                                //parent.location.reload();
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
    };
});