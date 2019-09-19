$(function () {
    $('#captcha-img').click(function (enevt) {
        var self=$(this)
        var src=self.attr('src')
        src=src+'?'
        self.attr('src',src)
    })
})

$(function () {
    $('#sms-captcha-btn').click(function (event) {
        event.preventDefault();
        var self=$(this);
        var telephone=$("input[name='telephone']").val();
        if(!(/^1[345879]\d{9}$/.test(telephone))){
            xtalert.alertInfoToast('请输入正确的手机号');
            return;
        }

        var timestamp=(new Date).getTime();
        var sign=md5(timestamp+telephone+'fgeWdLwg436t@$%$^');
        myajax.post({
            'url':'/c/sms_captcha/',
            'data':{
                'telephone':telephone,
                'timestamp':timestamp,
                'sign':sign
            },
            'success':function (data) {
                if (data['code']==200){
                    xtalert.alertSuccessToast(data['message']);
                    self.attr('disabled','disabled');
                    var timeCount=60;
                    var timer = setInterval(function () {
                        timeCount--;
                        self.text("正在发送(" + timeCount + ")");
                        if (timeCount<=0){
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text('再次发送验证码');
                        }
                    },1000);
                }
                else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    });

    // 不要忘记代码现加密后混淆!
});


$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var sms_captcha_input = $("input[name='sms_captcha']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var graph_captcha_input = $("input[name='graph_captcha']")

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        myajax.post({
            'url': '/i_forget/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'password1': password1,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            'success': function (data) {
                if (data['code'] === 200){
                    //修改密码成功后跳转到首页
                    setInterval(xtalert.alertSuccessToast(msg='密码修改成功，请重新登录'),5000)

                    window.location='/'

                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }

        });
    })
});

