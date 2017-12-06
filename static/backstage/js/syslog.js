layui.use(['layer', 'form', 'table', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        common = layui.common;

    var tableIns = table.render({
        elem: '#logTables',
        cols: [
            [{
                field: 'username', width: 150, title: '用户名', align: 'center',
            }, {
                field: 'nickname', width: 100, title: '昵称', align: 'center',
            }, {
                field: 'method', width: 80, title: '请求方法', align: 'center',
            }, {
                field: 'uri', width: 250, title: '请求URI', align: 'center',
            }, {
                field: 'data', width: 180, title: '请求数据', align: 'center',
            }, {
                field: 'ctime', width: 180, title: '时间', align: 'center',
            }]

        ],
        url: '/v1/opt_log/',
        page: true,
        even: true,
        id: 'logTables',
        limit: 30,
    });


    $('#larry_group .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });

    var active = {
        search: function () {
            var log_search = $('#log_search');
            //执行重载
            table.reload('logTables', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    username: log_search.val()
                }
            });
        }
    };
});