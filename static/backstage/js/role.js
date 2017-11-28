layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        common = layui.common;

    var tableIns = table.render({
        elem: '#roleTables',
        cols: [
            [{
                checkbox: true, width: 60, fixed: true
            }, {
                field: 'role_id', width: 80, title: 'ID', sort: true,
                // fixed: true
            }, {
                field: 'role_name', width: 200, title: '角色名', align: 'center',
            }, {
                field: 'status', width: 100, title: '状态', align: 'center', templet: '#switchTpl', unresize: true,
            }, {
                field: 'ctime', width: 235, title: '创建时间', align: 'center',
            }, {
                title: '常用操作', width: 260, align: 'center', toolbar: '#rolebar', fixed: "right"
            }]

        ],
        url: '/v1/accounts/role/',
        page: true,
        even: true,
        height: 'full-200',
        id: 'roleTables',
        limit: 10,
    });

    //监听表格复选框选择
    table.on('checkbox(roleTables)', function (obj) {
        console.log(obj)
    });

    //监听开关
    form.on('switch(sexDemo)', function (obj) {
        var data = obj.data;
        //layer.tips(this.value + this.name + '：' + obj.elem.checked, obj.othis);
        $.ajax({
            url: "/v1/accounts/role/",
            type: 'PATCH',
            data: JSON.stringify({"role_id": this.value}),
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
    table.on('tool(roleTables)', function (obj) {
        var data = obj.data;
        //console.log(data);
        if (obj.event === 'edit') {
            common.larryCmsMessage('角色不支持编辑', 'info');
            /* 角色不用编辑
            layer.confirm('确定要保存编辑吗？：' + data.role_name, function (index) {
                $.ajax({
                    url: "/v1/accounts/role/",
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
                    error: function (data) {
                        layer.msg(data.msg, {icon: 2, time: 1000});
                    },
                });
                layer.close(index);
                return false;
            });
            */
        } else if (obj.event === 'shouquan') {
            //layer.alert('授权行：<br>' + JSON.stringify(data))
            common.larryCmsMessage('最近好累，还是过段时间在写吧!', 'info');

        } else if (obj.event === 'del') {
            layer.confirm('删除行?', function (index) {
                var IdArr = [];
                IdArr.push(data.role_id);
                $.ajax({
                    url: "/v1/accounts/role/",
                    type: 'DELETE',
                    data: JSON.stringify({"role_id": IdArr}),
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
                content: '/static/backstage/html/user_manage/role_add.html',
                area: ['320px', '195px'],
                maxmin: true
            });
            layer.full(index);
        },
        search: function () {
            var role_search = $('#role_search');
            //执行重载
            table.reload('roleTables', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    role_name: role_search.val()
                }
            });
        },
        edit: function () {
            common.larryCmsMessage('最近好累，还是过段时间在写吧！,直接行内编辑吧', 'info');
        },
        del: function () {
            var checkStatus = table.checkStatus('roleTables'),
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
                                table.reload('roleTables', {
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