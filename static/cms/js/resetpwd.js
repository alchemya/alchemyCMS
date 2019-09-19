$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var oldpwdE = $('input[name=oldpwd]');
        var newpwdE = $('input[name=newpwd]');
        var newpwd2E= $('input[name=newpwd2]');

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        myajax.post({
            'url':'/cms/resetpwd/',
            'data':{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwd2':newpwd2
            },
            'success':function (args) {
                 if (args['code'] === 200){
                    //弹出成功的提示框，提示语是从后台传过来的message
                    xtalert.alertSuccessToast(args['message']);
                    oldpwdE.val('');   //完成请求后把表单输入的值清空
                    newpwdE.val('');
                    newpwd2E.val('');
                }else{
                    xtalert.alertError(args['message']);
                    oldpwdE.val('');
                    newpwdE.val('');
                    newpwd2E.val('');
                }
            },
            'fail':function (error) {
                xtalert.alertNetworkError('网络错误');
            }
        })
    })
})


