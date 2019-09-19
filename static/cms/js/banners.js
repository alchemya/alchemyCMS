$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self= $(this);
        var dialog = $("#banner-dialog");
        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");

        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        var submitType=self.attr('data-type');
        var bannerId=self.attr('data-id');
        var bannerId=$(this).attr('data-id')

        if(!name || !image_url || !link_url || !priority){
            xtalert.alertInfoToast('请输入完整的轮播图数据！');
            return;
        }
        var url='';
        if (submitType=='update'){
            url='/cms/update_banners/'
        }else {
            url='/cms/add_banners/'
        }

        myajax.post({
            "url": url,
            "data": {
                'name':name,
                'image_url': image_url,
                'link_url': link_url,
                'priority':priority,
                'banner_id':bannerId
            },
            'success': function (data) {
                // 隐藏对话框
                //dialog.modal("hide");
                if(data['code'] == 200){
                    // 重新加载这个页面
                    window.location.reload();
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                xtalert.alertNetworkError();
            }

        });
    });
});

$(function () {
    $('.edit-banner-btn').click(function (event) {
        var self= $(this);
        var dialog=$('#banner-dialog');
        dialog.modal('show');
        var tr=self.parent().parent();
        var name=tr.attr('data-name');
        var image_url=tr.attr('data-image');
        var link_url=tr.attr('data-link');
        var priority=tr.attr('data-priority');
        var data_id=tr.attr('data-id');

        var nameInput=$('input[name="name"]');
        var imageInput=$('input[name="image_url"]');
        var linkInput=$('input[name="link_url"]');
        var priorityInput=$('input[name="priority"]');
        var saveBtn=$('#save-banner-btn');

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr('data-type','update');
        saveBtn.attr('data-id',data_id);
    });
});

$(function () {
    $('.delete-banner-btn').click(function () {
        var self=$(this)
        var tr=self.parent().parent();
        var banner_id=tr.attr('data-id');
        // console.log(banner_id)
        xtalert.alertConfirm({
            'msg':'你需要删除这个轮播图吗',
            "confirmCallback":function () {
                myajax.post({
                    'url':'/cms/delete_banner/',
                    'data':{
                        'banner_id':banner_id
                    },
                    'success':function (data) {
                        if(data['code']==200){
                            window.location.reload();
                        }else {
                            xtalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        })
    });
});

$(function () {
    myqiniu.setUp({
        'domain':'http://pem47mau1.bkt.clouddn.com/',
                'browse_btn':'upload-btn',
                'uptoken_url':'/cms/uptoken/',
                'success':function (up,file,info) {
                    var imageInput=$("input[name='image_url']");
                    imageInput.val(file.name);
                }
    })
})