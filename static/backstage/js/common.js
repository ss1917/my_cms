layui.config({
	base: '/common/lib/'
});
layui.use(['jquery','layer','element','common','larryMenu','form'],function(){
	var $ = layui.$,
	layer = layui.layer,
	common = layui.common,
	device = layui.device(),
	form = layui.form,
	element = layui.element;
    // 页面上下文菜单
    larryMenu = layui.larryMenu();
	$('#larry_tab_content', parent.document).mouseout(function(){
         larryMenu.remove();
	});
});