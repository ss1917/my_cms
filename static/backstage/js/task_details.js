layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        laytpl = layui.laytpl,
        common = layui.common;

    //table.init('filter', options);
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

    $(function () {
        $.ajax({
            url: '/v1/task/sched/?list_id=' + list_id,
            success: function (data) {
                if (data.code == 0) {
                    layer.msg(data.msg, {icon: 1, time: 1000});
                    layer.closeAll('page');
                    all_data = JSON.stringify(data)
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




    var data = { //数据
        "title": "Layui常用模块",
        "list": [{"group": "1", "alias": "layer","hosts":['1','2']}, {"group": "2", "alias": "form","hosts":['1']}]
    }
    var getTpl = demo.innerHTML,
        view = document.getElementById('view');
    laytpl(getTpl).render(data, function (html) {
        view.innerHTML = html;
    });

    var tableIns = table.render({
        elem: '#tasklistTables',
        cols: [
            [{
                field: '', width: 60, title: '', sort: true,
            }, {
                field: 'task_level', width: 80, title: '优先级', align: 'center',
            }, {
                field: 'task_name', width: 150, title: '任务名称', align: 'center',
            }, {
                field: 'task_cmd', width: 200, title: '任务命令', align: 'center',
            }, {
                field: 'task_status', width: 80, title: '状态', align: 'center', templet: '#statusTpl', unresize: true,
            }, {
                title: '操作', width: 180, align: 'center', toolbar: '#publishbar', fixed: "right"
            }]
        ],
        url: '/v1/task/sched/?list_id=' + list_id,
        even: true,
        id: 'tasklistTables',
    });


    //监听表格复选框选择
    table.on('checkbox(userTables)', function (obj) {
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
    table.on('tool(tasklistTables)', function (obj) {
        var data = obj.data;
        if (obj.event === 'edit') {
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
        } else if (obj.event === 'shouquan') {
            //layer.alert('授权行：<br>' + JSON.stringify(data))
            common.larryCmsMessage('最近好累，还是过段时间在写吧!', 'info');

        } else if (obj.event === 'del') {
            layer.confirm('删除行?', function (index) {
                var IdArr = [];
                IdArr.push(data.user_id);
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
                                obj.del();
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
            var user_search = $('#user_search');
            console.log(user_search, user_search.val())
            //执行重载
            table.reload('userTables', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    username: user_search.val()
                }
            });
        },
        edit: function () {
            common.larryCmsMessage('最近好累，还是过段时间在写吧！,直接行内编辑吧', 'info');
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