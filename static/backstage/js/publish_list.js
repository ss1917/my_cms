layui.use(['layer', 'form', 'table', 'common', 'element',], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        common = layui.common,
        element = layui.element;

    //table.init('filter', options);
    var tableIns = table.render({
        elem: '#publishTables',
        cols: [
            [{
                field: 'user_id', width: 80, title: 'ID', sort: true,
                // fixed: true
            }, {
                field: 'username', width: 200, title: '项目名称', align: 'center',
            }, {
                field: 'username', width: 180, title: '应用名称', align: 'center',
            }, {
                field: 'username', width: 100, title: '提交人', align: 'center',
            }, {
                field: 'email', width: 100, title: '项目进度', align: 'center',
            }, {
                field: 'status', width: 100, title: '发布状态', align: 'center', templet: '#switchTpl', unresize: true,
            }, {
                field: 'last_login', width: 180, title: '开始时间', align: 'center',
            }, {
                field: 'last_login', width: 180, title: '计划完成时间', align: 'center',
            }, {
                title: '常用操作', width: 120, align: 'center', toolbar: '#publishbar', fixed: "right"
            }]

        ],
        url: '/v1/accounts/user/',
        page: true,
        even: true,
        height: 'full-200',
        id: 'publishTables',
        limit: 10,
    });

    var tableIns2 = table.render({
        elem: '#userTables',
        cols: [
            [{
                field: 'user_id', width: 80, title: 'ID', sort: true,
                // fixed: true
            }, {
                field: 'username', width: 200, title: '项目名称', align: 'center',
            }, {
                field: 'username', width: 180, title: '应用名称', align: 'center',
            }, {
                field: 'username', width: 100, title: '提交人', align: 'center',
            }, {
                field: 'status', width: 100, title: '发布状态', align: 'center', templet: '#switchTpl', unresize: true,
            }, {
                field: 'last_login', width: 180, title: '开始时间', align: 'center',
            }, {
                field: 'last_login', width: 180, title: '完成时间', align: 'center',
            }, {
                title: '常用操作', width: 120, align: 'center', toolbar: '#hisbar', fixed: "right"
            }]

        ],
        url: '/v1/accounts/user/',
        page: true,
        even: true,
        id: 'userTables',
        limit: 30,
    });

    /*
    $("[name=publishTables]").click(function () {
        table.reload("publishTables");
    });
    $("[name=userTables]").click(function () {
        table.reload("userTables");
    });
    */

    //监听工具条
    table.on('tool(userTables)', function (obj) {
        var data = obj.data;
        //console.log(data);
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
    };
});