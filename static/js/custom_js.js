$(document).ready(function(){
            //for subscription
            var Form = $('.subscriptionForm');
            var sspan = $('.news-subscribe');
            Form.submit(function(event){
                event.preventDefault();
                thisForm = $(this);
                var method = thisForm.attr('method');
                var endpoint = thisForm.attr('data-endpoint');
                var formData = thisForm.serialize();
                $.ajax({
                    url: endpoint,
                    method: method,
                    data: formData,
                    success: function(data){
                        sspan.html("<div class='row'><div class='col-12'>You have been successfully subscribed to our Newsletter...</div></div>");
                    },
                    error: function(errorData){
                        alert('An error occurred!<br>Please try again...');
                    },
                });
            });

            //For comment
            var commentForm = $('.commentForm');
            var commentFormSpan = $('.commentFormSpan');
            commentForm.submit(function(event){
                event.preventDefault();
                thisCommentForm = $(this);
                var method = thisCommentForm.attr('method');
                var endpoint = thisCommentForm.attr('data-endpoint');
                var formData = thisCommentForm.serialize();
                $.ajax({
                    url: endpoint,
                    method: method,
                    data: formData,
                    success: function(data){
                        if(data.done){
                            commentFormSpan.append("<div class='col-12 mt-3'><div class='alert' style='background-color:#F5FFFD;border-radius:17px!important;'><div class='toast-header'><img src='"+data.img_url+"' class='commentPhoto rounded mr-2'><strong class='mr-auto'>"+data.name+"</strong><small>"+data.day+"/"+data.month+"/"+data.year+"</small></div><div class='toast-body'>"+data.content+"</div></div></div>");
                            }else{
                                alert(data.message)
                            }
                        },
                    error: function(errorData){
                        alert('An error occurred! Please try again...');
                    },
                });
            });


           $('.navbar-toggler').click(function(event){
                $(".mobileMenu").toggleClass('open');
           })
           $(window).scroll(function() {
                var nav = $('#navbarMain');
                var mobile = $('#mobile')
                var top = 300;
                if ($(window).scrollTop() >= top) {
                    nav.addClass('coloured');
                    mobile.addClass('opaque');
                } else {
                    nav.removeClass('coloured');
                    mobile.removeClass('opaque');
                }
           });
           $('#searchBar-toggler').click(function(){
                $(".searchBar").toggleClass('show');
                $(window).scrollTop($('#topatbase').offset().top);
           });
            //For AutoSearch
            var searchForm = $('.searchForm');
            searchForm = $(this);
            var searchInput = searchForm.find(".search-input");
            var typingTimer;
            var typingInterval = 2000; //in millisecond
            var submitBtn = searchForm.find(".submitBtn");
            function performSearch(){
                doSearch();
                var query = searchInput.val();
                setTimeout(function(event){
                    window.location.href = "/search/?q=" + query;
                }, 3000)
            }
            function doSearch(){
                submitBtn.addClass("disabled")
                submitBtn.html("Searching <i class='fas fa-spinner fa-spin'></i>")
            }
            searchInput.keyup(function(event){
                // Key released
                clearTimeout(typingTimer)
                typingTimer = setTimeout(performSearch, typingInterval)
            })
            searchInput.keydown(function(event){
                // Key pressed
                clearTimeout(typingTimer)
            });
});