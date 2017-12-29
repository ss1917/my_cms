layui.use(['layer', 'form', 'table', 'laydate', 'common'], function () {
    var $ = layui.$,
        layer = layui.layer,
        form = layui.form,
        table = layui.table,
        laydate = layui.laydate,
        common = layui.common;

    var now = new Date();
    var date = new Date(now.getTime() - 7 * 24 * 3600 * 1000);
    var month = date.getMonth() + 1;
    var yizhou = date.getFullYear() + '-' + month + '-' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds()
    var tableIns = table.render({
        elem: '#logTables',
        cols: [
            [{
                field: 'username', width: 150, title: '用户名', align: 'center',
            }, {
                field: 'nickname', width: 120, title: '昵称', align: 'center',
            }, {
                field: 'method', width: 100, title: '请求方法', align: 'center',
            }, {
                field: 'uri', width: 250, title: '请求URI', align: 'center',
            }, {
                field: 'data', width: 400, title: '请求数据', align: 'center',
            }, {
                field: 'ctime', width: 180, title: '时间', align: 'center',
            }]

        ],
        url: '/v1/opt_log/?ctime='+yizhou,
        page: true,
        even: true,
        id: 'logTables',
        limit: 30,
    });

    laydate.render({
        elem: '#timedata',
        type: 'datetime',
        min: -180,
        value: yizhou,
    });

    $('#larry_group .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });

    var active = {
        search: function () {
            var log_search = $('#log_search');
            var timedata = $('#timedata');
            table.reload('logTables', {
                url: '/v1/opt_log/?username=' + log_search.val() + '&ctime=' + timedata.val(),
            });
        }
    };
});