layui.use(['layer', 'form', 'table', 'common', 'util', 'laydate'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        laytpl = layui.laytpl,
        util = layui.util,
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

    // 手动干预的任务
    var getTpl1 = task1.innerHTML,
        view1 = document.getElementById('view1');
    laytpl(getTpl1).render(data_init, function (html) {
        view1.innerHTML = html;
    });

    var thisTimer, setCountdown = function () {
        var endTime = new Date(data_init.task_time).getTime() //结束日期
            , serverTime = new Date(); //假设为当前服务器时间，这里采用的是本地时间，实际使用一般是取服务端的
        clearTimeout(thisTimer);
        util.countdown(endTime, serverTime, function (date, serverTime, timer) {
            var str = date[0] + '天' + date[1] + '时' + date[2] + '分' + date[3] + '秒';
            lay('#djs').html(str);
            thisTimer = timer;
        });
    };
    setCountdown();


    var tableIns = table.render({
        elem: '#taskdetailsTables',
        cols: [
            [{
                field: 'exec_ip', width: 180, title: '执行主机', align: 'center'
            }, {
                field: 'task_group', width: 80, title: '执行组', align: 'center'
            }, {
                field: 'task_level', width: 80, title: '优先级', align: 'center', sort: true
            }, {
                field: 'task_name', width: 150, title: '任务名称', align: 'center'
            }, {
                field: 'task_cmd', width: 200, title: '任务命令', align: 'center'
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
            var index = layer.open({
                type: 2,
                content: '/static/backstage/templates/task/task_log.html?list_id=' + data.list_id + '&exec_ip=' + data.exec_ip + '&task_group=' + data.task_group + '&task_level=' + data.task_level,
                area: ['320px', '195px'],
                anim: 1,
                title: '日志',
                maxmin: true,
                end: function () {

                }
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
        all_hand: function () {
            var input_value = [];
            $(this).siblings().each(function (index, item) {
                input_value.push($(item).val());
            });
            var hand_task = input_value[0];
            layer.confirm('确定执行所有：' + hand_task + '？？？', function (index) {
                $.ajax({
                    url: "/v1/task/sched/",
                    type: 'PUT',
                    data: JSON.stringify({
                        "list_id": list_id,
                        "hand_task": hand_task,
                        "task_handle": "all_hand"
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
                    error: function () {
                        layer.msg('失败', {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
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