$(function () {
    $('#btn').click(function (event) {
        event.preventDefault();
        var email = $('input[name=email]').val();
        if(!email){
            xtalert.alertInfoToast('请输入邮箱');
            return;
        }

        var obj = $("#btn")
        settime(obj);


        myajax.get({
            'url': '/cms/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['code'] === 200){
                    xtalert.alertSuccessToast(data['message']);


                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }
        })
    })
});
var countdown=60;


function settime(obj) { //发送验证码倒计时

    if (countdown == 0) {
        obj.attr('disabled',false);
        //obj.removeattr("disabled");
        obj.val("获取验证码");
        countdown = 60;
        return;
    } else {
        obj.attr('disabled',true);
        obj.val("重新发送(" + countdown + ")");
        countdown--;
    }
setTimeout(function() {
    settime(obj) }
    ,1000)
}

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var emailE = $('input[name=email]');
        var captchaE = $('input[name=captcha]');

        var email = emailE.val();
        var captcha = captchaE.val();

        myajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] === 200){
                    xtalert.alertSuccessToast(data['message']);
                    emailE.val('');
                    captchaE.val('');
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }
        })
    })
});