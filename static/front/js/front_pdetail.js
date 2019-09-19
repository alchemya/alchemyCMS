$(function(){

    var ue=UE.getEditor('editor',{
        'serverUrl':'/ueditor/upload/',
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'blockquote', //引用
                'selectall', //全选
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
    });
    window.ue=ue;
});

$(function(){
   $('#comment-btn').on('click',function(event){
       event.preventDefault();
       var login_tag=$('#login-tag').attr('data-is-login');
       if (! login_tag){
           window.location='/login/'
       }else{
           var content=window.ue.getContent();
           var post_id=$('#post-content').attr('data-id');
           myajax.post({
              'url':'/add_comment/' ,
               'data':{
                  'content':content,
                   'post_id':post_id
               },
               'success':function(data){
                  if(data['code']==200){
                      xtalert.alertSuccessToast(msg='评论发表成功');
                      window.location.reload();
                  }else{
                        xtalert.alertInfo(data['message']);
                  }
               }
           });
       }

   }) ;
});