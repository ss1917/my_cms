layui.use(['tree', 'layer', 'table'], function () {
    var layer = layui.layer,
        table = layui.table,
        $ = layui.jquery;


    var tableIns = table.render({
        elem: '#menuTables',
        cols: [
            [{
                field: 'id', width: 80, title: 'ID', align: 'center'
            }, {
                field: 'name', width: 100, title: '名称', align: 'center', edit: 'text'
            }, {
                field: 'font', width: 100, title: '字体', align: 'center', edit: 'text'
            }, {
                field: 'icon', width: 120, title: '图标', align: 'center', edit: 'text', sort: true
            }, {
                field: 'url', width: 280, title: 'url', align: 'center', edit: 'text'
            }, {
                field: 'sort', width: 100, title: '排序', align: 'center', edit: 'text'
            }, {
                title: '操作', width: 220, align: 'center', toolbar: '#menubar', fixed: "right"
            }]
        ],
        url: '/v1/accounts/menu/?nav=list',
        even: true,
        page: false,
        id: 'menuTables',
    });

    var data_init = null;
    $(function () {
        $.ajax({
            url: '/v1/accounts/menu/?nav=list',
            async: false,
            success: function (data) {
                if (data.code == 0) {
                    layer.msg(data.msg, {icon: 1, time: 1000});
                    layer.closeAll('page');
                    data_init = data.data;
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

    layui.tree({
        elem: '#menu_tree' //指定元素
        , target: '_blank' //是否新选项卡打开（比如节点返回href才有效）
        , click: function (item) { //点击节点回调
            table.reload('menuTables', {
                url: "/v1/accounts/menu/?menu_id=" + item.id,
            });

            //layer.msg('当前节名称：' + item.name + '<br>全部参数：' + JSON.stringify(item));
            //console.log(item);
        }
        , nodes: data_init
    })
    ;

});