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
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var graph_captcha_input = $("input[name='graph_captcha']")

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        myajax.post({
            'url': '/signup/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'username': username,
                'password1': password1,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            'success': function (data) {
                if (data['code'] === 200){
                    //注册成功跳转到首页
                    xtalert.alertSuccessToast('注册成功')
                    var return_to = $('#return-to-span').text()
                    if (return_to){
                        window.location=return_to
                    }else {
                        window.location='/'
                    }
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

