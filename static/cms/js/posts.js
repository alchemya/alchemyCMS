$(function(){
    $('.highlight-btn').on('click',function(){
       var $this=$(this);
       var tr=$this.parent().parent();
       var post_id=tr.attr('data-id');
       console.log(post_id)
       var highlight=parseInt(tr.attr('data-highlight'));
       var url='';
        if(highlight){
           url='/cms/uhpost/'
        }else{
            url='/cms/hpost/'
        }
        myajax.post({
            'url':url,
            'data':{
                'post_id':post_id
            },
            'success':function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast('操作成功');
                    setTimeout(function(){
                        window.location.reload();
                    },500);
                }else{
                    xtalert.alertInfo(data['message']);
                }
            }
        })
    });
});