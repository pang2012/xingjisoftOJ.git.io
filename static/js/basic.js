window.onbeforeunload = function() {
	const params = new URLSearchParams(window.location.search);
    // 设置你想传递的参数
    var parameter = params.get('username');
 
    // Flask路由URL
    var route = '/close_page';
 
    // 使用fetch API发送请求
    fetch(route, {
        method: 'POST', // 使用POST方法
        headers: {
            'Content-Type': 'application/json' // 设置请求头为JSON
        },
        body: JSON.stringify({ parameter: parameter }) // 将参数作为JSON发送
    })
    .then(response => response.json()) // 解析响应（如果需要）
    .then(data => console.log(data)) // 处理解析后的数据
    .catch(error => console.error('Error:', error)); // 错误处理
};