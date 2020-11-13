//========================super class======================================
var utility = {};
var bookCoverId;
utility = {
	getCookie:function(name)
	{
    			var cookieValue = null;
    			if (document.cookie && document.cookie !== '') {
        			var cookies = document.cookie.split(';');
        			for (var i = 0; i < cookies.length; i++) {
            			var cookie = jQuery.trim(cookies[i]);
            			// Does this cookie string begin with the name we want?
            		if (cookie.substring(0, name.length + 1) === (name + '=')) {
                		cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                	break;
            	}
        	}
    	}
    return cookieValue;

	},

	addbookcover:function()
	{
        var fileLength = $('input[type=file]')[0].files.length;
        var file = $('input[type=file]')[0].files[0];
    	var userid = $(".global").text();
    	var form = $("#bookCover")[0];
    	var fd = new FormData(form);
		fd.append('created_by', userid);

        if(fileLength>0){  
		  fd.append('image',file);
        }
        else{
          fd.append('url',$('#myImg').attr("src"));    
        }

    	$.ajax({
		    url: '/threadcard/api/addbookcover/',
		    data: fd,
		    type: 'POST',
		    contentType: false,
		    processData: false,
            headers: {
                'X-CSRFToken': csrftoken
            }, 
		    success:function(res){
		    	bookCoverId = res;
                utility.addThreadBit(res.id);
		    }
		});
	},

    GetUs:function(value){
        return value;  //this is used for any where temp value declarations just like constructor
    },

    listThread:function(cardID)
    {
        $.getJSON("/threadcard/api/listthread/"+cardID,function(result){
            
            $.each(result,function(key,value){
                if(value.bookcoverowner==userIdValue){     //check valid user
                    $('.addThreadBit').before("<div class='timeline-event'> <div class='card timeline-content'> <div class='card-panel z-depth-1'> <div class='row valign-wrapper'> <div class='col s12'> <span style='display:none;' class='threadId'>"+value.id+"</span> <div class='thread-comment'>"+value.message+"</div> </div> </div> <div style='margin-bottom:4%;'><div class='left'><a class='black-text displayCrud' style='cursor:pointer;font-size:18px;' title='click to edit or delete this thread'><i style='font-size:18px;vertical-align:-.125em;' class='material-icons'>more_horiz</i></a><a class='tooltipped black-text edit' style='display:none;' data-position='top' data-delay='50' data-tooltip='Edit'><i style='font-size:18px;vertical-align:-.125em;' class='material-icons'>mode_edit</i></a> &nbsp;<a class='tooltipped black-text modal-trigger deleteBit' href='#modal1' data-position='top' data-delay='50' data-delete-id='"+value.id+"' style='display:none;' data-tooltip='delete'><i style='font-size:18px;vertical-align:-.125em;' class='material-icons'>delete</i></a></div> </div> </div> </div> </div>");

                    // <div class='right'><a id='annotate-link"+value.id+"' class='tooltipped black-text annotate-link' data-position='top' data-delay='50' data-tooltip='annotate'><i class='far fa-comment-alt'></i></a></div> add this to side message icon
                }
                else{
                    $('.addThreadBit').before("<div class='timeline-event'> <div class='box-none card timeline-content margin-0 bg-transparent'> <div class='box-none card-panel z-depth-1 margin-0 border-one'> <div class='row valign-wrapper'> <div class='col s12'> <span style='display:none;' class='threadId'>"+value.id+"</span> <div class='thread-comment'>"+value.message+"</div> </div> </div> <div style='margin-bottom:4%;'></div> </div> </div> </div>");

                    // <div class='right'><a id='annotate-link"+value.id+"' class='tooltipped black-text annotate-link' data-position='top' data-delay='50' data-tooltip='annotate'><i class='far fa-comment-alt'></i></a></div> add this to side message icon
                }
            });
        });
    },

	addThreadBit:function(coverID)
	{
    	var threadBitLength = $('.whatSay').length,threadBit = [];
    	var userid = $(".global").text();
    	var threadBitInfo={};

    	for(var i=0;i<threadBitLength;i++){

            if($.trim($('.whatSay')[i].value)!=""){

                threadBitInfo = {

                    "bookcover":coverID,
                    "bookcoverowner":userid,
                    "message":$.trim($('.whatSay')[i].value)

                }

    		    threadBit.push(threadBitInfo);
            }
            
    	}

    	$.ajax({
		    url: '/threadcard/api/createthread/',
		    data: JSON.stringify(threadBit),
		    type: 'POST',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken
            }, 
		    success:function(res){
		    	$('#modal1').modal('open');
		    }
		});

	},

	editThreadBit:function(msg,threadId,userid,bookCoverId)
	{
    	var threadBitInfo={};

		threadBitInfo = {
		    "message": msg,
		    "bookcoverowner":userid,
		    "bookcover":bookCoverId,
		};
    		
    	$.ajax({
		    url: '/threadcard/api/editthread/'+threadId+'/',
		    data: JSON.stringify(threadBitInfo),
		    type: 'PUT',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken
            }, 
		    success:function(res){
		    }
		});

	},

    deleteThreadBit:function(deleteid){
        $.ajax({
            url: '/threadcard/api/deletethread/'+deleteid,
            type: 'DELETE',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken
            }, 
            success: function(result) {
            }
        });
    },

    addSingleThreadBit:function(msg,bookcoverownerId,cardId){
        var userid = $(".global").text();

        var threadBit = {
          "message": msg,
          "bookcoverowner": bookcoverownerId,
          "bookcover": cardId
          }


        $.ajax({
            url: '/threadcard/api/addthread/',
            data: JSON.stringify(threadBit),
            type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
            }
        });
    },

    addSubComment:function(userID,threadID,comment){
        
        var userid = $(".global").text();

        var threadBit = {
          "comment": comment,
          "threadname":threadID,
          "created_by":userID
          }

        // console.log(threadBit);

        $.ajax({
            url: '/threadcard/api/addsubcomment/',
            data: JSON.stringify(threadBit),
            type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
            }
        });
    },

    listSubComment:function(threadID){
        var userid = $(".global").text();
        $.getJSON('/threadcard/listsubcomment/'+threadID+'/',function(result){
            $(".profile_list a").remove();
            $.each(result,function(key,value){
                $('.profile_list').append('<a href=""><img height="35" width="35" src="'+value.user_profile+'" alt="" class="circle"></a>');
            });
                $(".testcontent li").remove();
                if($(".testcontent p").length>0){
                    $(".testcontent p").remove();     
                }
                if(result.length<=0){
                    $(".testcontent ul").append("<p><i>Be the first one to comment.</i></p>");
                }
            $.each(result,function(key,value){
                $(".testcontent ul").append(" <li class='commentline' style='font-size:14px;'><a class='black-text' href=''><b>"+value.commented_user+" </b></a><span>"+value.comment+"</span></li>");
            });
        });
    },

    addEntireComment:function(comment,bookcoverid,userID){
        
        var userid = $(".global").text();

        var threadBit = {
          "comment": comment,
          "bookcover":bookcoverid,
          "rater":userID
          }

        // console.log(threadBit);

        $.ajax({
            url: '/threadcard/api/addrating/',
            data: JSON.stringify(threadBit),
            type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
            }
        });

    },
    subscribeAction:function(toggle,creator_id,user_id){

        var subscribeToggle = {
            "subscribe":(toggle=='true')?true:false,
            "writter":user_id,
            "reader":creator_id
        }


        $.ajax({
            url: '/threadcard/api/subscribe/',
            data: JSON.stringify(subscribeToggle),
            type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
                utility.listSubscribers(res.reader);
                Materialize.toast('Cool! You have subscribed this Creator!', 3000);
                $('.subscribeButton').attr('data-subscribe-id',res.id);
                $('.subscribeButton').css({"background-color":'#3db974',"color":'#fff','border-color':'#3db974'});
                $('.subscribeButton').empty().html("Subscribed&nbsp;<i class='fas fa-check'></i>");
            }
        });

    },
    checkSubscribe:function(from ,to){
        $.ajax({
            url: '/threadcard/api/checksubscribe/'+from+'/'+to+'/',
            type: 'GET',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
                (res.length==0)?$('.subscribeButton').attr('data-subscribe-id',''):$('.subscribeButton').attr('data-subscribe-id',res[0].id);
                if(res.length==0){
                    $('.subscribeButton').attr('data-subscribe-id','');
                    $('.subscribeButton').css({"background-color":'#fff',"color":'#ec5120','border-color':'#ec5120'});
                    $('.subscribeButton').empty().html("Subscribe <i class='far fa-hand-point-up'></i>");
                }
                else{
                    $('.subscribeButton').attr('data-subscribe-id',res[0].id);
                    $('.subscribeButton').css({"background-color":'#3db974',"color":'#fff','border-color':'#3db974'});
                    $('.subscribeButton').empty().html("Subscribed<i class='fas fa-check'></i>");
                }
            }
        });
    },
    unSubscribeAction:function(creatorid,unsubscribeid){

        $.ajax({
            url: '/threadcard/api/unsubscribe/'+unsubscribeid+'/',
            type: 'DELETE',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
                utility.listSubscribers(creatorid);
                Materialize.toast('You have unsubscribed this Creator!', 3000);
                $('.subscribeButton').attr('data-subscribe-id','');
                $('.subscribeButton').css({"background-color":'#fff',"color":'#ec5120','border-color':'#ec5120'});
                $('.subscribeButton').empty().html("Subscribe <i class='far fa-hand-point-up'></i>");
            }
        });

    },
    listSubscribers:function(creatorId){
        $.getJSON('/threadcard/api/listsubscribers/'+creatorId,function(result){
            if(result.length>0){
                $('.noOfSubscribers').text(result.length);
                $('.subscribeListBox').empty();
                $.each(result,function(key,value){
                    $(".subscribeListBox").append("<li class='collection-item'><div class='subscribeImage'><img class='circle' src='"+value.user_profile+"'></div><div class='subscriberName'>"+value.username+"</div></li>");
                }); 
            }
            else{
                $('.noOfSubscribers').text(result.length);
                $('.subscribeListBox').empty();
                $(".subscribeListBox").append("<li class='collection-item'>There are no subscribers for this creator.</li>");
            }
        });
    },
    // '<a href='#!' class='subscribeListButton secondary-content'>subscribe</a>' for future use
    createDeleteBlock:function(){
        $('.deleteBlock').append("<div id='modal1' class='modal'> <div class='modal-content'> <h4> <i class='material-icons'>info_outline</i> Alert</h4> <p style='line-height:25px;'>Are you sure you want to delete this thread bit?<br/><b><u>Warning:</u></b> This will also delete related comments.</p> </div> <div class='modal-footer'> <a href='#!' data-delete-ack='' class='modal-action modal-close waves-effect waves-green btn-flat deleteConfirm'>Confirm</a> </div> </div>");
    },
    listCard:function(userid){

        $.getJSON('/threadcard/perticularthreadList/'+userid,function(result){
          result = result.bookcover_data.reverse();
          console.log(result);
          $.each(result,function(key,value){
                if(value.likes>0){
                    if(value.liked==true){

                        // $('.listThread').append("<li class='collection-item avatar'>"+"<div title='Read this thread' class='card horizontal List'>"+"<div class='card-image' style='width:170px;'>"+"<a href='/"+value.created_by+"/"+value.bookcoverid+"'>"+"<img class='responsive-img' style='width:170px;' src='"+value.image+"' alt=''></a></div>"+"<div class='card-stacked'><div data-thread-id='"+value.bookcoverid+"' class='card-content thread-content'><p>"+value.name+"</p></div>"+"<div class='likeSection card-action'><div class='right'><div data-bookcover-id='"+value.bookcoverid+"' data-like-id='0' class='heart is_animating'><span class='likeCount'>"+value.likes+"</span></div></div></div>"+"</div></div></li>").reverse();                        

                        $('.gridThread').append(" <div class='col l3'> <div title='Read this thread' class='card hoverable' style='box-shadow:4px 4px 20px #b1b1b154;'> <div class='card-image'><a href='/"+value.created_by+"/"+value.bookcoverid+"'><img style='height:250px;' src='"+value.image+"'></a></div><div class='card-content _new-block-content'><div class='row mb-0'><a href='#!' data-creator='"+value.created_userid+"' data-bookcover-id='"+value.bookcoverid+"' data-like-id='0' class='col s6 center-align likeToggle'><span>"+value.likes+"</span> <i class='fas fa-heart' style='color:#FF0047;'></i></a><a href='/"+value.created_by+"/"+value.bookcoverid+"' class='col s6 center-align'>"+value.same_threads_created_by.length+" <i class='fas fa-code-branch'></i></a></div></div></div> </div>").reverse();

                    }
                    if(value.liked==false){

                        // $('.listThread').append("<li class='collection-item avatar'>"+"<div title='Read this thread' class='card horizontal List'>"+"<div class='card-image' style='width:170px;'>"+"<a href='/"+value.created_by+"/"+value.bookcoverid+"'>"+"<img class='responsive-img' style='width:170px;' src='"+value.image+"' alt=''></a></div>"+"<div class='card-stacked'><div data-thread-id='"+value.bookcoverid+"' class='card-content thread-content'><p>"+value.name+"</p></div>"+"<div class='likeSection card-action'><div class='right'><div data-bookcover-id='"+value.bookcoverid+"' data-like-id='0' class='heart'><span class='likeCount'>"+value.likes+"</span></div></div></div>"+"</div></div></li>").reverse();

                        $('.gridThread').append(" <div class='col l3'> <div title='Read this thread' class='card hoverable' style='box-shadow:4px 4px 20px #b1b1b154;'> <div class='card-image'><a href='/"+value.created_by+"/"+value.bookcoverid+"'><img style='height:250px;filter:brightness(80%);' src='"+value.image+"'></a></div><div class='card-content _new-block-content'><div class='row mb-0'><a href='#!' data-creator='"+value.created_userid+"' class='col s6 center-align likeToggle'><span>"+value.likes+"</span><i class='far fa-heart'></i></a><a href='/"+value.created_by+"/"+value.bookcoverid+"' data-bookcover-id='"+value.bookcoverid+"' data-like-id='0' class='col s6 center-align'>"+value.same_threads_created_by.length+" <i class='fas fa-code-branch'></i></a></div></div></div> </div>").reverse();

                    }

                }
                if(value.likes==0){

                    // $('.listThread').append("<li class='collection-item avatar'>"+"<div title='Read this thread' class='card horizontal List'>"+"<div class='card-image' style='width:170px;'>"+"<a href='/"+value.created_by+"/"+value.bookcoverid+"'>"+"<img class='responsive-img' style='width:170px;' src='"+value.image+"' alt=''></a></div>"+"<div class='card-stacked'><div data-thread-id='"+value.bookcoverid+"' class='card-content thread-content'><p>"+value.name+"</p></div>"+"<div class='likeSection card-action'><div class='right'><div data-bookcover-id='"+value.bookcoverid+"' data-like-id='0' class='heart'><span class='likeCount'></span></div></div></div>"+"</div></div></li>").reverse();

                    $('.gridThread').append(" <div class='col l3'> <div title='Read this thread' class='card hoverable' style='box-shadow:4px 4px 20px #b1b1b154;'> <div class='card-image'><a href='/"+value.created_by+"/"+value.bookcoverid+"'><img style='height:250px;' src='"+value.image+"'></a></div><div class='card-content _new-block-content'><div class='row mb-0'><a href='#!' data-creator='"+value.created_userid+"' class='col s6 center-align likeToggle' data-bookcover-id='"+value.bookcoverid+"' data-like-id='0'><i class='far fa-heart'></i></a><a href='/"+value.created_by+"/"+value.bookcoverid+"' class='col s6 center-align'>"+value.same_threads_created_by.length+" <i class='fas fa-code-branch'></i></a></div></div></div> </div>").reverse();                    
                }
          });
        });
    },
    likeThread:function(bookcoverid){
        $.getJSON('/threadcard/likethread/'+bookcoverid,function(result){
            $(".heart").each(function(){
                if(result[0].bookcover_id==$(this).attr("data-bookcover-id")){
                    $(this).addClass("is_animating");
                    $(this).attr("data-like-id",1);
                }
            });
        });
    },
    unlikeThread:function(bookcoverid){
        $.getJSON('/threadcard/unlikethread/'+bookcoverid,function(result){
            $(".heart").each(function(){
                if(result[0].bookcover_id==$(this).attr("data-bookcover-id")){
                    $(this).removeClass("is_animating");
                    $(this).attr("data-like-id",0);
                }
            });
        });
    },
    listSubscribedCreators:function(userid){

        $.getJSON('/threadcard/api/subscribedlist/'+userid,function(result){
            $('.noOfSubscribed').text(result.length);
          $.each(result,function(key,value){    
            $('.subscribedCreatorsList').append(" <div class='col m4'> <div style='padding-top:10px;padding-bottom:10px;' class='card-panel white'> <div style='margin-bottom: 10px;' class='row valign-wrapper'> <div class='col s9'> <h4>"+value.username+"</h4> <a href='https://twitter.com/"+value.username+"' target='_blank'>@"+value.username+"</a> </div> <div class='col s3'> <a href='https://twitter.com/"+value.username+"' target='_blank'> <img src='"+value.user_profile+"' alt='' class='circle responsive-img'> </a> </div> </div> <div style='margin-bottom: 0;' class='row'> <div class='col s4'> <p style='margin-top:0;margin-bottom:0;'><span style='font-weight:bold;font-size:20px;'><a href='#!'>0</a></span> threads</p> </div> <div class='col s3'></div> <div class='col s4'> <a href='#!' style='font-weight:bold;font-size:20px;'>0</a> <span>subscribers</span> </div> </div> </div> </div>");
                
            $(".subscribedBox").append("<div class='Label card-panel white'> <div style='margin-bottom: 10px;' class='row valign-wrapper'> <div class='col s9'> <h5>"+value.username+" <a href='https://twitter.com/"+value.username+"' style='font-size:15px;' target='_blank'><i class='fab fa-twitter'></i></a> </h5> </div> <div class='col s3'> <a href='https://twitter.com/"+value.username+"' target='_blank'> <img src='"+value.user_profile+"' alt='' class='circle responsive-img'> </a> </div> </div> <div style='margin-bottom: 0;' class='row'> <div class='col s4'> <p style='margin-top:0;margin-bottom:0;'><span style='font-weight:bold;'><a href='#!' class='myReadBooks' title='click to view no of threads'>0</a></span> threads</p> </div> <div class='col s6'> <a class='noOfSubscribed' title='click to view your subscribers' style='font-weight:bold;' href='#!'>0</a> <span>subscribers</span> </div> </div> </div>");
          });
        });

    },
    submitFeedbackForm:function(username,userid,email,comment){

        var feedback = {
          "email":email,
          "username":username,
          "comment":comment,
          "url":window.location.href,
          "created_by":userid
          }


        $.ajax({
            url: '/threadcard/api/addfeedback/',
            data: JSON.stringify(feedback),
            type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
                $("#feedback1").modal('open');
                $("#feedbackfromvalue")[0].reset();
                $(".chat-box").hide();
            }
        });

    },
    searchBookList:function(query){
    	var query = query.replace(/\s/g,'');
        $.getJSON('/api/searchbooks/'+query+'/',function(result){
            $(".searchDropBox").empty();
            $(".globalBookSearchDropBox").find('li').remove();
          if(result.length<1){
            Materialize.toast('Book name '+query+' not found', 3000);
          }  
          else{
              $.each(result,function(key,value){
                $(".searchDropBox").append("<li title='Click to add this bookCover' class='collection-item avatar searchBoxContainer'> <img class='searchResultBookCover circle' src='"+value.bookImage+"' alt='"+value.booktitle+"' style='border-radius:0;'> <span class='title'>"+value.booktitle+"</span> <p>"+value.bookauthor+"<br>"+value.bookpublisher+"</p></li>");

                $(".searchDropBox").show();

                $(".globalBookSearchDropBox").append("<li title='Click to add this bookCover' class='collection-item avatar globalSearchBoxContainer'><div class='globalSearchResult'><img class='globalSearchResultBookCover circle' src='"+value.bookImage+"' alt='"+value.booktitle+"' style='border-radius:0;'> <span class='title'>"+value.booktitle+"</span> <p class='bookAuthor'>"+value.bookauthor+"</p><p class='bookPublisher'>"+value.bookpublisher+"</p></div><div class='ReadStatus center-align'><div style='margin-bottom:5px;padding-bottom:5px;'>Select Status</div> <p> <input class='readCheck with-gap' name='group"+key+"' type='radio' id='test"+key+1+"' checked/> <label for='test"+key+1+"'>Read </label> <input class='readingCheck with-gap' name='group"+key+"' type='radio' id='test"+key+2+"'/> <label for='test"+key+2+"'>Reading </label> <input class='tobeCheck with-gap' name='group"+key+"' type='radio' id='test"+key+3+"'/> <label for='test"+key+3+"'>To Be Read</label> </p></div></li>");

                $(".globalBookSearchDropBox").show();

                $(".podcastSearchDropBox").append("<li title='Click to add this bookCover' class='collection-item avatar globalSearchBoxContainer'><div class='globalSearchResult'><img class='globalSearchResultBookCover circle' src='"+value.bookImage+"' alt='"+value.booktitle+"' style='border-radius:0;'> <span class='title'>"+value.booktitle+"</span> <p class='bookAuthor'>"+value.bookauthor+"</p><p class='bookPublisher'>"+value.bookpublisher+"</p></div></li>");

                $(".podcastSearchDropBox").show();            
              });
            }
        });

    },
    addBookStatus:function(bookImage,bookTitle,bookAuthor,bookPublisher,readCheck,readingCheck,tobeCheck,userid){
        var readStatus = {
          "image":bookImage,
          "bookname":bookTitle,
          "author":bookAuthor,
          "publisher":bookPublisher,
          "user":userid,
          "toberead":tobeCheck,
          "read":readCheck,
          "reading":readingCheck
          }

        $.ajax({
            url: '/threadcard/api/adduserintreset/',
            data: JSON.stringify(readStatus),
            type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
            	// console.log(res);
            }
        });

    },
    addPodcast:function(name,embed,creatorid){
        var podcast = {
            "name":name,
            "embed":embed,
            "created_by":creatorid
        }

        $.ajax({
            url: '/threadcard/api/addpodcast/',
            data: JSON.stringify(podcast),
            type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
                localStorage.setItem("pod", res.id);
                Materialize.toast('Podcast created!!', 2000);
            }
        });        
    },
    addPodcastBooks:function(bookImage,bookTitle,bookAuthor,bookPublisher,userid){
        var readStatus = {
          "image":bookImage,
          "bookname":bookTitle,
          "author":bookAuthor,
          "publisher":bookPublisher,
          "user":userid,
          "podcast":localStorage.getItem("pod")
          }

        $.ajax({
            url: '/threadcard/api/addpodcastbooks/',
            data: JSON.stringify(readStatus),
            type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
                localStorage.setItem("pod", "");
            }
        });
    },
    deletePodcast:function(pcard,userid){
        var _pid = $(pcard).attr("data-p");
        $(pcard).parent().parent().parent().parent().parent().remove();  

        $.ajax({
            url: '/threadcard/api/deletepodcast/'+_pid,
            type: 'DELETE',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken
            }, 
            success: function(result) {
                $("._listPodcasts").empty();
                utility.listPodcast(userid);
            }
        });
    },
    listPodcast:function(userid){
        $.getJSON('/threadcard/api/listpodcast/'+userid+'/',function(result){

            if(result.length>0){
                $(".createPodcast").css("display","block");
                $.each(result,function(key,value){
                    var cid = btoa(value.created_by.id);
                    var uname = btoa(value.created_by.username);
                    var pname = btoa(value.name);
                    var plink = btoa(value.embed);
                    var pid = btoa(value.id);
                    if(value.embed.startsWith("<iframe")){
                        $("._listPodcasts").append("<div class='col s6'> <div class='card podcastListCard'> <div class='card-content'> <div class='podcast-list-section'><div class='right _toolList'><a href='#!' data-p='"+value.id+"' class='podcastDel'><i class='fa fa-trash'></i></a><a href='/podcastshare/?aa="+cid+"&ab="+uname+"&ac="+plink+"&ad="+pid+"&ae="+pname+"' class='podcastShare'><i class='fa fa-link'></i></a></div></div><img src='http://pbs.twimg.com/profile_images/1040270850207797248/d_A90Ye5_normal.jpg' class='circle'><br/><p style='font-size:14px;font-family:Karla-Bold,san-serif'>"+value.name+"</p>"+value.embed+"<a href='#!' data-p='"+value.id+"' style='font-size:14px;' class='_podcastBookLinks'></a><div class='booklists row'></div></div></div> </div> </div>");
                    }
                    else if(value.embed.startsWith("https://")){
                        $("._listPodcasts").append("<div class='col s6'> <div class='card podcastListCard'> <div class='card-content'> <div class='podcast-list-section'><div class='right _toolList'><a href='#!' data-p='"+value.id+"' class='podcastDel'><i class='fa fa-trash'></i></a><a href='/podcastshare/?aa="+cid+"&ab="+uname+"&ac="+plink+"&ad="+pid+"&ae="+pname+"' class='podcastShare'><i class='fa fa-link'></i></a></div><img src='http://pbs.twimg.com/profile_images/1040270850207797248/d_A90Ye5_normal.jpg' class='circle'><br/><p style='font-size:14px;font-family:Karla-Bold,san-serif'>"+value.name+"</p><a href='#!' data-p='"+value.id+"' style='font-size:14px;' class='_podcastBookLinks'></a><div class='booklists row'></div></div> </div> </div> </div>");

                    }
                });
                    $("._podcastBookLinks").each(function(key,value){
                        utility.listPodcastBooks(this);
                    });
            }
            else{
                $(".createPodcast").css("display","none");
                $("._listPodcasts").append("<h5 class='center-align'>You Haven't added any podcasts.<a href='/createpodcast/'> Click here to Add Some.</a></h5>")
            }
        });        
    },
    listPodcastBooks:function(podcastbooklink){

        var _blank = $(podcastbooklink).attr("data-p");
        $.getJSON('/threadcard/listpodcastbooks/'+_blank+'/',function(result){
            $(podcastbooklink).next().empty();
            if(result.length>0 && result.length<=3){                
                $.each(result,function(key,value){
                    var persona = btoa(value.image);
                    var personi = btoa(value.bookname);
                    var persoid = btoa(value.id);
                    if(value.same_threads_created_by.length>0){
                        $(podcastbooklink).next().append("<div class='col s4'><a href='/"+value.username+"/createlist/?aj="+personi+"&gh="+persona+"' target='_blank' title='write thread from this book'><div class='card'> <div class='card-image'> <img style='height:100px;' src='"+value.image+"'/> </div><div class='card-content podcastBookThreadsCount'>"+value.same_threads_created_by.length+" <i class='fas fa-code-branch'></i></div></div></a></div>");
                    }
                    else{
                        $(podcastbooklink).next().append("<div class='col s4'><a href='/"+value.username+"/createlist/?aj="+personi+"&gh="+persona+"' target='_blank' title='write thread from this book'><div class='card'> <div class='card-image'> <img style='height:100px;' src='"+value.image+"'/> </div><div class='card-content podcastBookThreadsCount'></div></div></a></div>");

                    }
                });
            }
            else if(result.length>3){     
                for(var i=0;i<3;i++){ 
                    var persona = btoa(result[i].image);
                    var personi = btoa(result[i].bookname);
                    var persoid = btoa(result[i].id);
                    if(result[i].same_threads_created_by.length>0){
                        $(podcastbooklink).next().append("<div class='col s4'><a href='/"+result[i].username+"/createlist/?aj="+personi+"&gh="+persona+"' target='_blank' title='write thread from this book'><div class='card'> <div class='card-image'> <img style='height:100px;' src='"+result[i].image+"'/> </div><div class='card-content podcastBookThreadsCount'>"+result[i].same_threads_created_by.length+" <i class='fas fa-code-branch'></i></div></div></a></div>");
                    }
                    else{
                        $(podcastbooklink).next().append("<div class='col s4'><a href='/"+result[i].username+"/createlist/?aj="+personi+"&gh="+persona+"' target='_blank' title='write thread from this book'><div class='card'> <div class='card-image'> <img style='height:100px;' src='"+result[i].image+"'/> </div><div class='card-content podcastBookThreadsCount'></div></div></a></div>");

                    }
                }
                    $(podcastbooklink).next().append("<a href='"+$(podcastbooklink).parent().find("._toolList>.podcastShare").attr("href")+"'>View More</a>");
            }
            else{
                    $(podcastbooklink).next().append("<li>There are no books referred</li>");
            }
        });

    },
    listPodcastBooksShare:function(podcastbooklink){
        var _blank = $(podcastbooklink).attr("data-p");
        $.getJSON('/threadcard/listpodcastbooks/'+_blank+'/',function(result){
            $(".podCastShareBooks").empty();
            console.log(result);
            if(result.length>0){                
                $.each(result,function(key,value){
                    var persona = btoa(value.image);
                    var personi = btoa(value.bookname);
                    var persoid = btoa(value.id);
                    // $(".podCastShareBooks").append("<li class='_lists'><a href='/"+value.user.username+"/createlist/?aj="+personi+"&gh="+persona+"' target='_blank' title='write thread from this book'>"+value.bookname+"</a></li>");
                    if(value.same_threads_created_by.length>0){
                        $(".podCastShareBooks").append("<div class='col s3'><a href='/"+value.username+"/createlist/?aj="+personi+"&gh="+persona+"' target='_blank' title='write thread from this book'><div class='card'> <div class='card-image'> <img style='height:150px;' src='"+value.image+"'/> </div><div class='card-content podcastBookThreadsCount'>"+value.same_threads_created_by.length+" <i class='fas fa-code-branch'></i></div> </div></a></div>");
                    }
                    else{
                        $(".podCastShareBooks").append("<div class='col s3'><a href='/"+value.username+"/createlist/?aj="+personi+"&gh="+persona+"' target='_blank' title='write thread from this book'><div class='card'> <div class='card-image'> <img style='height:150px;' src='"+value.image+"'/> </div><div class='card-content podcastBookThreadsCount'></div> </div></a></div>");

                    }
                });
            }
            else{
                    $(".podCastShareBooks").append("<li>There are no books referred</li>");
            }
        });    
        // console.log("<div class='col s3'><a href=''><div class='card'> <div class='card-image'> <img src='http://books.google.com/books/content?id=TJZi36MBs6UC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'/> </div> </div></a></div>");
    },
    listBookStatus:function(userid){

        $.getJSON('/threadcard/api/listuserintresetbyuserread/'+userid+'/',function(result){
            $('.readTagSection').empty();

            if(result.length>0){
                // $('.readTagSection').parent().show();
            	$.each(result,function(key,value){
                    var persona = btoa(value.image);
                    var personi = btoa(value.bookname);
                    var persoid = btoa(value.id);

                    $(".readTagSection").append("<div class='col l3'> <div title='Read this thread' class='card hoverable' style='box-shadow:4px 4px 20px #b1b1b154;'> <div class='card-image'><a href=''><img style='height:250px;' src='"+value.image+"'></a></div><div class='card-content _new-block-content'><p class='bookellipsis'>"+value.bookname+"</p><div style='text-align:center;'><a title='Start thread on this book' href='/sriharsha_k95/createlist/?aj="+personi+"&gh="+persona+"'><i class='material-icons bookStatusPanel'>timeline</i></a></div></div></div> </div>").reverse();
           		});	
            }
            else{
                $('.readTagSection').append("<p style='padding:0 .75rem;'><i>This section has no read books.</i></p>");
            }
        });

        $.getJSON('/threadcard/api/listuserintresetbyuserreading/'+userid+'/',function(result){
            $('.readingTagSection').empty();

            if(result.length>0){
                // $('.readingTagSection').parent().show();
            	$.each(result,function(key,value){
                    var persona = btoa(value.image);
                    var personi = btoa(value.bookname);

                    $(".readingTagSection").append("<div class='col l3'> <div title='Reading in Progress' class='card hoverable' style='box-shadow:4px 4px 20px #b1b1b154;'> <div class='card-image'><a href=''><img style='height:250px;' src='"+value.image+"'></a></div><div class='card-content _new-block-content'><p class='bookellipsis'>"+value.bookname+"</p><div style='text-align:center;'><a title='Start thread on this book' href='/sriharsha_k95/createlist/?aj="+personi+"&gh="+persona+"'><i class='material-icons bookStatusPanel'>timeline</i></a>&nbsp;&nbsp;<a href='#!' data-reading-state="+value.reading+" data-tobe-state="+value.toberead+" data-read-state="+value.read+" data-id="+value.id+" class='statusChange' title='Finished Reading'><i class='material-icons bookStatusPanel'>class</i></a></div></div></div> </div>").reverse();
           		});
            }
            else{
                $('.readingTagSection').append("<p style='padding:0 .75rem;'><i>You haven't started reading any books.</i></p>");
            }

        });

        $.getJSON('/threadcard/api/listuserintresetbyusertoberead/'+userid+'/',function(result){
            $('.toBeTagSection').empty();

            if(result.length>0){
                // $('.toBeTagSection').parent().show();

                $.each(result,function(key,value){
                    var persona = btoa(value.image);
                    $(".toBeTagSection").append("<div class='col l3'> <div title='Start Reading' class='card hoverable' style='box-shadow:4px 4px 20px #b1b1b154;'> <div class='card-image'><a href=''><img style='height:250px;' src='"+value.image+"'></a></div><div class='card-content _new-block-content'><p class='bookellipsis'>"+value.bookname+"</p><div style='text-align:center;'><a href='#!' data-reading-state="+value.reading+" data-tobe-state="+value.toberead+" data-read-state="+value.read+" data-id="+value.id+" class='statusChange' title='Start Reading'><i class='material-icons bookStatusPanel'>import_contacts</i></a></div></div></div> </div>").reverse();
                });
            }

            else{
                $('.toBeTagSection').append("<p style='padding:0 .75rem;'><i><a href='/'>Add</a> some books to start reading.</i></p>");;
            }

        });
    },
    changeBookStatus:function(readStatus,readingStatus,tobeStatus,bookId,userid){
        
        tobeStatus = (tobeStatus=='true')?true:false;
        readStatus = (readStatus=='true')?true:false;
        readingStatus = (readingStatus=='true')?true:false;     

        if(readingStatus==true){

            var bookStatus = {
                "toberead":false,
                "read":true,
                "reading":false,
                "user": userid
            };

        }
        if(tobeStatus==true){
            
            var bookStatus = {
                "toberead":false,
                "read":false,
                "reading":true,
                "user": userid
            };

        }


        $.ajax({
            url: '/threadcard/api/getuserintreset/'+bookId+'/',
            data: JSON.stringify(bookStatus),
            type: 'PATCH',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                }, 
            success:function(res){
                if(res.read==true){
                    Materialize.toast('You have finished reading '+res.bookname, 3000);
                }
                if(res.reading==true){
                    Materialize.toast('You have Started reading '+res.bookname, 3000);
                }
                utility.listBookStatus(userid);
            }
        });

    }

};

//===============get csrf token through cookie======================================


var csrftoken = utility.getCookie('csrftoken');

//======================input file replace by image==================================
    $(function () {

        $(":file").change(function () {
          	    
            if($('#topic_name').val()!=""){
                $('.createThread').removeClass('disabled');
            }

            if (this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = imageIsLoaded;
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    function imageIsLoaded(e) {
        $('#myImg').attr('src', e.target.result);
    }


//=====================================search paradigm===========================================   

    $(document).on('keypress','#topic_name',function(e){
        // e.preventDefault();
        if(e.which==13){
            if($.trim($(this).val())==""){
              Materialize.toast('Enter Book Name', 1000);
            }
            else{   
                $(".searchDropBox").empty().append("<li class='collection-item avatar'>Loading</li>");
                utility.searchBookList($(this).val());
            }
        }
    });

    $(document).on('click','.SearchButton',function(){
        if($.trim($("#topic_name").val())==""){
          Materialize.toast('Enter Book Name', 1000);
        }
        else{   
            $(".searchDropBox").empty().append("<li class='collection-item avatar'>Loading</li>");
            utility.searchBookList($("#topic_name").val());
        }
    });    

    $(document).on('click','.searchBoxContainer',function(){
        $("#myImg").attr("src",$(this).find('.searchResultBookCover').attr("src"));
        $("#topic_name").val($(this).find('.searchResultBookCover').attr("alt"));
        $('.searchDropBox').hide();
        $('.createThread').removeClass('disabled');
        $('html, body').animate({
            scrollTop: $(".createThread").offset().top
        }, 2000);
    });

    $("#bookCover").submit(function(e){
        e.preventDefault();
    });

    $(document).on('keyup','#topic_name',function(){
        if($(this).val()!="" && $(':file')[0].files.length){
            $('.createThread').removeClass('disabled');
        }
        else{
            $('.createThread').addClass('disabled'); 
        }
    });

//=================add book cover and start threads bits=============================

    $(document).on('click','.createThread',function(){
    	// utility.addbookcover();
        $('.timeline-event').last().after(" <div class='timeline-event'> <div class='card timeline-content'><i class='closeThis right material-icons'>close</i><div class='card-panel z-depth-1'><div class='row valign-wrapper'><div class='input-field col s12'> <textarea class='whatSay materialize-textarea' maxlength=200 id='input_text' type='text' data-length='200'></textarea><label for='input_text'>What you say?</label> </div>  <div class='fixed-action-btn horizontal click-to-toggle'><ul><li><a class='btn-floating green tooltipped' data-delay='50' data-position='top' data-tooltip='image'><i class='material-icons'>image</i></a></li> <li><a class='btn-floating blue tooltipped' data-delay='50' data-position='top' data-tooltip='Video'><i class='material-icons'>movie</i></a></li> </ul> </div></div></div></div></div><div class='right'><a class='next waves-effect waves-light btn-flat disabled'>Next</a> <a  class='threadIt waves-effect waves-light btn-flat disabled'>Thread It</a></div>");
        $(this).addClass('disabled');

        $('input, textarea').characterCounter();
    });

//================================add threadbits=======================================

    $(document).on('click','.next',function(){
        $('.timeline-event').last().after("<div class='timeline-event'><div class='card timeline-content'><i class='closeThis right material-icons'>close</i><div class='card-panel z-depth-1'><div class='row valign-wrapper'><div class='input-field col s12'><textarea class='whatSay materialize-textarea' id='input_text' type='text' maxlength=200 data-length='200'></textarea></div></div></div></div></div>");
    $('.tooltipped').tooltip({delay: 50});

        $('input, textarea').characterCounter();

        if($('.whatSay').last().val().length==0){
            $('.next').addClass('disabled');
        }
    });

//=================================threadIT action==========================================

    $(document).on('click','.threadIt',function(){
    	utility.addbookcover();
    });

//================enable next button action on char length=================================

    $(document).on('keyup','.whatSay',function(){

      if($(this).length==1 && $(this).is('.whatSay:last') && $.trim($(this).last().val()).length==0){
        $('.next').addClass('disabled');
        $('.threadIt').addClass('disabled');  
      }
      else{
          $('.next').removeClass('disabled');
          $('.threadIt').removeClass('disabled');        
      }
      // else if($(this).val().length>200){
      //   $('.timeline-event').last().after("<div class='timeline-event'><div class='card timeline-content'><i class='closeThis right material-icons'>close</i><div class='card-panel z-depth-1'><div class='row valign-wrapper'> <div class='col s2'><img src='http://materializecss.com/images/yuna.jpg' alt='' class='circle responsive-img'> </div> <div class='input-field col s10'><textarea class='whatSay materialize-textarea' id='input_text' type='text' data-length='200'></textarea> <label for='input_text'>What you say?</label></div></div></div></div></div>");
      // }
    });

//========================delete threadBit if unnecessary when opened new block =============================(P.S this is not for fully created threadbit)

    $(document).on('click','.closeThis',function(){
        $(this).parent().parent().remove();
        if($('.whatSay').length==1 && $('.whatSay').is('.whatSay:last') && $.trim($('.whatSay').last().val()).length==0){
            $('.next').addClass('disabled');
            $('.threadIt').addClass('disabled');  
        }
        if($('.whatSay').length==0){
          $('.next').remove();
          $('.threadIt').remove();
          $('.createThread').removeClass('disabled');
        }
    });

//==================junk needed stilll==============================================
    
    $(function(){
      utility.createDeleteBlock();  
      $('.modal').modal();  
      $(".button-collapse").sideNav();
      $('.carousel.carousel-slider').carousel({fullWidth: true});

    });

//================feedback Toggle==============================================

      $(document).on('click','.feedBackForm',function(){
          $('.chat-box').toggle();
      });

      $(document).on('click','.closeChatBox',function(){
        $('.chat-box').hide();
      });