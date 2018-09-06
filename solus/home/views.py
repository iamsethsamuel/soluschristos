from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . forms import *
from django.http import HttpResponseNotFound, HttpResponse
from django.core.serializers import serialize


def homepage(request):
    if request.user.is_authenticated:
        subSubscribedID = [s for s in Subscription.objects.filter(subscriber=request.user).values_list(
            "subscribe", flat=True)]
        postList = []
        posts = []
        suggested = suggested_users(request)
        for user in subSubscribedID:
            postList.append(Posts.objects.filter(creator=user).order_by("-date"))
        for post in postList:
            for p in post:
                posts.append(p)
        paginator = Paginator(posts, 4)
        p_page = request.GET.get("page")
        try:
            post = paginator.page(p_page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(1)
        if request.is_ajax():
            return render(request, "home/postAjax.html", {"posts": post})
        else:
            return render(request, "home/posts_list.html", {"posts": post,"suggested_users":suggested})
    else:
        return render(request, "home/welcome.html")


def suggested_users(request):
    already_following = Subscription.objects.filter(subscriber=request.user.username).exclude(
        subscribe=request.user)
    suggested_users = Users.objects.filter(stateRegion=request.user.users.stateRegion).exclude(user=request.user)
    suggested = []
    following = []
    suggestions = []
    for users in already_following:
        following.append(users.subscribe.username)
    for user in suggested_users:
        suggested.append(user.user.username)
    for suggestion in suggested:
        if suggestion not in following:
            suggestions.append(Users.objects.filter(user__username=suggestion))
    return suggestions


def notification(request):
    userSubcribed = [s for s in Subscription.objects.filter(subscriber=request.user).values_list("subscribe", flat=True)]
    userSubscribes= []
    notificationsList = []
    notifications = []
    for user in userSubcribed:
        userSubscribes.append(User.objects.get(id=user).id)
    for user in userSubscribes:
        notificationsList.append(Notifications.objects.filter(user=user).exclude(user=request.user))
    if Notifications.objects.filter(notified_user=request.user):
        notificationsList.append(Notifications.objects.filter(notified_user=request.user).exclude(user=request.user))
    for i in notificationsList:
        for ex in i:
            notifications.append(ex)
    paginator = Paginator(notifications, 5)
    page = request.GET.get("page")
    try:
        notification = paginator.page(page)
    except EmptyPage:
        notification = paginator.page(1)
    except PageNotAnInteger:
        notification = paginator.page(1)
    return render(request, "home/notifications.html", {"notifications": notification, "length": len(notifications)})


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            items = form.cleaned_data.get("search")
            profiles = User.objects.filter(username__icontains=items).order_by("username")
            posts = Posts.objects.filter(content__icontains=items).order_by("-date")
            postsPaginator = Paginator(posts, 5)
            profilesPaginator = Paginator(profiles,5)
            profilepage = request.GET.get("profilesearch")
            postpage = request.GET.get("postpage")
            try:
                prof = profilesPaginator.get_page(profilepage)
                post = postsPaginator.get_page(postpage)
            except PageNotAnInteger:
                post =postsPaginator.get_page(1)
                prof = profilesPaginator.get_page(1)
            except EmptyPage:
                post = postsPaginator.get_page(1)
                prof = profilesPaginator.get_page(1)

            if post or prof:
                if request.is_ajax():
                    return render(request, 'home/searchajax.html', {'posts': post, 'prof': prof})
                else:
                    return render(request, 'home/search.html', {'posts': post, 'prof': prof})
            else:
                return render(request, 'home/searchajax.html', {"error":"No result found"})
    else:
        return redirect('home:index')


def signup(request):
    from django.contrib.auth import login, authenticate
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        c_password = request.POST.get("c_password")
        email = request.POST.get("email")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        country = request.POST.get("country")
        stateRegion = request.POST.get("stateRegion")
        dp = request.FILES.get("dp")
        sex = request.POST.get("sex")
        if c_password == password:
            auth_username = request.POST.get("username")
            auth_password = request.POST.get("password")
            User.objects.create_user(username=username,password=password,email=email, first_name=firstName,last_name=lastName)
            users = User.objects.get(username=username)
            Users.objects.create(user=users, dob=dob, phone=phone, country=country, stateRegion=stateRegion,
                                    dp=dp, sex=sex)
            user = authenticate(request, username=auth_username, password=auth_password)
            login(request,user)
            Subscription.objects.create(subscriber=auth_username, subscribe=users)
            return redirect("home:home")
    else:
        import datetime
        return render(request, 'home/signup.html', {"date":datetime.date.today().year - 14})


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("home:login")


def profile(request, username):
    try:
        userid = User.objects.get(username=username).id
        profile = User.objects.get(username=username)
        followers = Subscription.objects.filter(subscribe=userid).count()
        user = User.objects.get(id=userid)
        following = Subscription.objects.filter(subscriber=user).count()
        raw_posts = Posts.objects.filter(creator_id=userid).order_by("-date")
        if Subscription.objects.filter(subscriber=request.user, subscribe=userid):
            allreadyFollowing = Subscription.objects.get(subscriber=request.user, subscribe=userid).subscriber
        else:
            allreadyFollowing = ""
        paginator = Paginator(raw_posts, 10)
        page = request.GET.get("profilepost")
        subscribe = Subscription.objects.filter(subscriber=request.user)
        try:
            post = paginator.get_page(page)
        except PageNotAnInteger:
            post = paginator.get_page(1)
        except EmptyPage:
            post = paginator.get_page(1)
        if request.is_ajax():
            return render(request, "home/profileajax.html", {"posts": post})
        return render(request, "home/profiles.html", {"posts": post, "followers": followers, "following": following,
                                                      "profile": profile, "subscribe": subscribe,"alreadyFollowing":

                                                      allreadyFollowing, "username":username})
    except User.DoesNotExist:
        return HttpResponseNotFound("<h1>Page Not Found</h1>")


def update_profile(request, username):
    import datetime
    if request.method == "POST":
        def posted(item):
            if item:
                return item
            else:
                return ""
        Subscription.objects.filter(subscribe=User.objects.get(username=request.user), subscriber=request.user.username)
        User.objects.filter(username=request.user.username).update(first_name=posted(request.POST['first_name']),
                            last_name=posted(request.POST['last_name']), email=posted(request.POST['email']))
        Users.objects.filter(user=User.objects.get(username=username)).update(dob=posted(request.POST['dob']),stateRegion
        =posted(request.POST['stateRegion']), country=posted(request.POST['country']), sex=posted(request.POST['sex']))

        return redirect("home:profile", username)

    return render(request, 'home/userdetails.html', {"date": datetime.date.today().year - 14})


def createFollow(request, username):
    user = User.objects.get(username=username)
    Subscription.objects.create(subscribe=user, subscriber=request.user)
    Notifications.objects.create(user=request.user, item="{} has stated following you".format(str(user.username).title()),
                                 notified_user=user.username)
    return redirect("home:profile", user.username)


def unFollow(request,userid):
    user = User.objects.get(id=userid)
    Subscription.objects.get(subscribe=user, subscriber=request.user).delete()
    # Notifications.objects.get(user=request.user, item="{} stated following you".format(str(user.username).title()),
    #                              notified_user=user).delete()
    return redirect("home:profile", user.username)


def comments(request, post_id):
    comment = Comment.objects.filter(post_id=post_id).order_by("-date")
    return render(request, "home/comments.html", {"comments": comment})


def createComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        postId = request.POST.get("post")
        post = Posts.objects.get(id=postId)
        Comment.objects.create(comment=comment, post_id=postId, user=request.user)
        Notifications.objects.create(item="{} comments has commented on your post".format(str(request.user).title()),
                                     user=request.user, notified_user=post.creator)
        return HttpResponse("Success")
    else:
        return redirect("/")


def createLike(request):
    if request.method == "POST":
        formPost = request.POST["post"]
        post = Posts.objects.get(id=formPost)
        Like.objects.create(post=post, user=request.user)
        Notifications.objects.create(item="{} has liked your post".format(str(request.user).title()),
                                     user=request.user, notified_user=post.creator,post=post)
        return HttpResponse("Success")
    else:
        return redirect("/")


def unLike(request):
    if request.method == "POST":
        formPost = request.POST["post"]
        post = Posts.objects.get(id=formPost)
        Like.objects.get(post=post, user=request.user).delete()
        Notifications.objects.get(item="{} has liked your post".format(str(request.user).title()),
                                  user=request.user, notified_user=post.creator, post=post).delete()
        return HttpResponse("Sucess")
    else:
        return redirect("/")


def createPost(request):
    if request.method == "GET":
        if User.is_anonymous:
            return redirect("home:login")
    if request.method == "POST":
        creator = request.user
        content = request.POST.get("content")
        pic = request.FILES.get("pic")
        pic1 = request.FILES.get("pic1")
        pic2 = request.FILES.get("pic2")
        pic3 = request.FILES.get("pic3")
        pic4 = request.FILES.get("pic4")
        pic5 = request.FILES.get("pic5")
        pic6 = request.FILES.get("pic6")
        pic7 = request.FILES.get("pic7")
        pic8 = request.FILES.get("pic8")
        pic9 = request.FILES.get("pic9")
        import re
        import os

        def ffmpeg(file):
            import subprocess
            import shlex
            pipe = subprocess.PIPE
            fmt = file.name[-3:]
            file.name = re.sub("[\W]","",file.name,flags=re.S)
            file.name = file.name.replace(fmt,"")
            file.name = file.name.replace("\n","")
            cmd = 'ffmpeg -t 10:0 -i "init{}.{}" -vf "scale=-2:720" -y -vf "scale=-2:240" "144{}.mp4" "{}.mp4"'\
                .format(file.name, fmt, file.name, file.name)
            picture = 'ffmpeg -t 2 -i init{}.{} -frames 1 -y {}.jpg'.format(file.name, fmt, file.name)
            shlex.quote(cmd)
            shlex.quote(cmd)
            with open("init{}.{}".format(file.name, fmt), "wb") as f:
                for chunk in file.chunks():
                    f.write(chunk)
            ffm = subprocess.run(cmd, stderr=pipe, stdout=pipe, shell=True)
            if ffm.stderr:
                print("ffm error \n", ffm.stderr)
            shakaPackager = "packager in={}.mp4,stream=audio,output=audio{}.mp4 in={}.mp4,stream=video,output=shaka{}.mp4" \
                            " in=144{}.mp4,stream=video,output=shaka144{}.mp4  --mpd_output {}.mpd".format(file.name,
                                    file.name, file.name, file.name,file.name,file.name, file.name)
            shaka = subprocess.run(shakaPackager, shell=True, stdout=pipe, stderr=pipe)
            subprocess.run(picture, shell=True)
            if shaka.stderr:
                print("shaka error \n",shaka.stderr)
            os.remove("init{}.{}".format(file.name,fmt))
            os.remove("{}.{}".format(file.name,fmt))
            os.remove("144{}.{}".format(file.name, fmt))

        def uploadFile(file):
            if file.name.endswith("jpeg") or file.name.endswith("jpg") or file.name.endswith("png"):
                return file
            else:
                return "uploads/{}.mpd".format(file.name)

        if pic9:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic9, pic8, pic7, pic6, pic5, pic4, pic3, pic2, pic1, pic]
                for file in files:
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        ffmpeg(file)

                post = Posts.objects.create(creator=creator, content=content,pic9=uploadFile(pic9), pic8=uploadFile(pic8),
                                            pic7=uploadFile(pic7),pic6=uploadFile(pic6), pic5=uploadFile(pic5),
                                            pic4=uploadFile(pic4),pic3=uploadFile(pic3), pic2=uploadFile(pic2),
                                            pic1=uploadFile(pic1), pic=uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post, item="{} has posted".format(request.user))
                os.chdir("../../../..")
            except:
                pass

        elif pic8:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic8, pic7, pic6, pic5, pic4, pic3, pic2, pic1, pic]
                for file in files:
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        ffmpeg(file)

                post = Posts.objects.create(creator=creator, content=content,pic8=uploadFile(pic8), pic7=uploadFile(pic7),
                                            pic6=uploadFile(pic6), pic5=uploadFile(pic5), pic4=uploadFile(pic4),
                                            pic3=uploadFile(pic3), pic2=uploadFile(pic2), pic1=uploadFile(pic1), pic=
                                            uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post, item="{} has posted".format(request.user))

                os.chdir("../../../..")
            except:
                pass
        elif pic7:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic7, pic6 ,pic5, pic4, pic3, pic2, pic1, pic]
                for file in files:
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        ffmpeg(file)

                post = Posts.objects.create(creator=creator, content=content, pic7=uploadFile(pic7),pic6=uploadFile(pic6),
                                            pic5=uploadFile(pic5), pic4=uploadFile(pic4), pic3=uploadFile(pic3),
                                            pic2=uploadFile(pic2), pic1=uploadFile(pic1), pic=uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post, item="{} has posted".format(request.user))
                os.chdir("../../../..")
            except:
                pass
        elif pic6:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic6, pic5, pic4, pic3, pic2, pic1, pic]
                for file in files:
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        ffmpeg(file)

                post = Posts.objects.create(creator=creator, content=content,pic6=uploadFile(pic6), pic5=uploadFile(pic5),
                                            pic4=uploadFile(pic4),pic3=uploadFile(pic3), pic2=uploadFile(pic2),
                                            pic1=uploadFile(pic1),pic=uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post,item="{} has posted".format(request.user))
                os.chdir("../../../..")
            except:
                pass
        elif pic5:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic5, pic4, pic3, pic2, pic1, pic]
                for file in files:
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        ffmpeg(file)
                post = Posts.objects.create(creator=creator, content=content, pic5=uploadFile(pic5),pic4=uploadFile(pic4),
                                    pic3=uploadFile(pic3), pic2=uploadFile(pic2), pic1=uploadFile(pic1),pic=uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post, item="{} has posted".format(request.user))

                os.chdir("../../../..")
            except:
                pass
        elif pic4:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic4, pic3, pic2, pic1, pic]
                for file in files:
                        ffmpeg(file)
                post = Posts.objects.create(creator=creator, content=content, pic4=uploadFile(pic4), pic3=uploadFile(pic3),
                                            pic2=uploadFile(pic2), pic1=uploadFile(pic1), pic=uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post,item="{} has posted".format(request.user))

                os.chdir("../../../..")
            except:
                pass
        elif pic3:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic3, pic2, pic1, pic]
                for file in files:
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        ffmpeg(file)

                post = Posts.objects.create(creator=creator, content=content,pic3=uploadFile(pic3), pic2=uploadFile(pic2),
                                            pic1=uploadFile(pic1), pic=uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post, item="{} has posted".format(request.user))

                os.chdir("../../../..")
            except:
                pass
        elif pic2:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic2, pic1, pic]
                for file in files:
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        ffmpeg(file)

                post = Posts.objects.create(creator=creator, content=content, pic2=uploadFile(pic2), pic1=uploadFile(pic1),
                                            pic=uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post, item="{} has posted".format(request.user))

                os.chdir("../../../..")
            except:
                pass
        elif pic1:
            try:
                os.chdir("home/static/uploads/uploads")
                files = [pic1, pic]
                for file in files:
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        ffmpeg(file)
                post = Posts.objects.create(creator=creator, content=content, pic1=uploadFile(pic1), pic=uploadFile(pic))
                Notifications.objects.create(user=request.user, post=post,item="{} has posted".format(request.user))
                os.chdir("../../../")
            except:
                pass
        elif pic:
            try:
                os.chdir("home/static/uploads/uploads")
                if pic.name.endswith("mp4") or pic.name.endswith("avi"):
                    ffmpeg(pic)
                    post = Posts.objects.create(creator=creator, content=content, pic="uploads/{}.mpd".format(pic.name))
                else:
                    post = Posts.objects.create(creator=creator, content=content, pic=pic)
                Notifications.objects.create(user=request.user, post=post, item="{} has posted".format(request.user))
                os.chdir("../../../..")
            except:
                pass
        else:
            post = Posts.objects.create(creator=creator, content=content)
            Notifications.objects.create(user=request.user, post=post, item="{} has posted".format(str(request.user)
                                                                                                   .title()))
        return redirect("home:home")
    else:
        return render(request, 'home/posts_form.html')


def postDetails(request, post_id):
    import datetime
    likes = Like.objects.filter(post=post_id).count()
    ccount = Comment.objects.filter(post_id= post_id).count()
    comment_list = Comment.objects.filter(post=post_id).order_by("-date")
    comment_page = Paginator(comment_list, 5)
    c_page = request.GET.get("comment")
    try:
        comments = comment_page.get_page(c_page)
        post = Posts.objects.filter(id=post_id)
    except EmptyPage:
        comments = comment_page.get_page(1)
    except PageNotAnInteger:
        comments = comment_page.get_page(1)
    except Posts.DoesNotExist:
        raise HttpResponseNotFound("Opps sorry post can't be found")
    return render(request, "home/postdetail.html", {"posts": post, "likes": likes, "ccount": ccount,
                                                    "comments":comments,"date":datetime.date.today()})

def deletePost(request):
    if request.method == "POST":
        del_id = request.POST.get("id")
        Posts.objects.get(id=del_id, creator=request.user).delete()
        Posts.objects.filter(id=del_id, creator=request.user)
        return redirect("home:home")
    else:
        return redirect("home:home")

def updatePost(request, id):
    if request.method == "POST":
        content = request.POST.get("content")
        pic = request.FILES.get("pic")
        pic1 = request.FILES.get("pic1")
        pic2 = request.FILES.get("pic2")
        pic3 = request.FILES.get("pic3")
        pic4 = request.FILES.get("pic4")
        pic5 = request.FILES.get("pic5")
        pic6 = request.FILES.get("pic6")
        pic7 = request.FILES.get("pic7")
        pic8 = request.FILES.get("pic8")
        pic9 = request.FILES.get("pic9")
        import os
        import re
        def ffmpeg(file):
            import subprocess
            import shlex
            pipe = subprocess.PIPE
            fmt = file.name[-3:]
            file.name = re.sub("[\W]", "", file.name, flags=re.S)
            file.name = file.name.replace(fmt, "")
            file.name = file.name.replace("\n", "")
            cmd = 'ffmpeg -t 10:0 -i "init{}.{}" -vf "scale=-2:720" -y -vf "scale=-2:240" "144{}.mp4" "{}.mp4"' \
                .format(file.name, fmt, file.name, file.name)
            shlex.quote(cmd)
            with open("init{}.{}".format(file.name, fmt), "wb") as f:
                for chunk in file.chunks():
                    f.write(chunk)
            ffm = subprocess.run(cmd, stderr=pipe, stdout=pipe, shell=True)
            if ffm.stderr:
                print("ffm error \n")
            shakaPackager = "packager in={}.mp4,stream=audio,output=audio{}.mp4 in={}.mp4,stream=video,output=shaka{}.mp4" \
                            " in=144{}.mp4,stream=video,output=shaka144{}.mp4  --mpd_output {}.mpd".format(
                file.name,
                file.name, file.name, file.name, file.name, file.name, file.name)
            shaka = subprocess.run(shakaPackager, shell=True, stdout=pipe, stderr=pipe)
            # subprocess.run(pic_cmd,shell=True)
            if shaka.stderr:
                print("shaka error \n")
            os.remove("init{}.{}".format(file.name, fmt))
            os.remove("{}.{}".format(file.name, fmt))
            os.remove("144{}.{}".format(file.name, fmt))

        def uploadFile(file):
            if file.name.endswith("jpeg") or file.name.endswith("jpg") or file.name.endswith("png"):
                with open(file.name, "wb") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return "uploads/{}".format(file.name)
            else:
                return "uploads/{}.mpd".format(file.name)
        if pic9:
            os.chdir("home/static/uploads/uploads")
            files = [pic9, pic8, pic7, pic6, pic5, pic4, pic3, pic2, pic1, pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    with open(file.name, "wb") as f:
                        for data in file.chunks():
                            f.write(data)
                    ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1), pic2=
                                uploadFile(pic2), pic3=uploadFile(pic3), pic4=uploadFile(pic4), pic5=uploadFile(pic5)
                                 , pic6=uploadFile(pic6), pic7=uploadFile(pic7), pic8=uploadFile(pic8), pic9=
                                 uploadFile(pic9))
            os.chdir("../../../..")
        elif pic8:
            os.chdir("home/static/uploads/uploads")
            files = [pic8, pic7, pic6, pic5, pic4, pic3, pic2, pic1, pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    with open(file.name, "wb") as f:
                        for data in file.chunks():
                            f.write(data)
                    ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1), pic2=
                                uploadFile(pic2), pic3=uploadFile(pic3), pic4=uploadFile(pic4), pic5=uploadFile(pic5)
                                 , pic6=uploadFile(pic6), pic7=uploadFile(pic7), pic8=uploadFile(pic8))
            os.chdir("../../../..")
        elif pic7:
            os.chdir("home/static/uploads/uploads")
            files = [pic7, pic6, pic5, pic4, pic3, pic2, pic1, pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    with open(file.name, "wb") as f:
                        for data in file.chunks():
                            f.write(data)
                    ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1), pic2=
                                 uploadFile(pic2), pic3=uploadFile(pic3), pic4=uploadFile(pic4), pic5=uploadFile(
                                pic5), pic6=uploadFile(pic6), pic7=uploadFile(pic7))
            os.chdir("../../../..")

        elif pic6:
            os.chdir("home/static/uploads/uploads")
            files = [pic6, pic5, pic4, pic3, pic2, pic1, pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    with open(file.name, "wb") as f:
                        for data in file.chunks():
                            f.write(data)
                    ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1), pic2=
                                 uploadFile(pic2), pic3=uploadFile(pic3), pic4=uploadFile(pic4), pic5=uploadFile(
                                 pic5), pic6=uploadFile(pic6))
            os.chdir("../../../..")

        elif pic5:
            os.chdir("home/static/uploads/uploads")
            files = [pic5, pic4, pic3, pic2, pic1, pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    with open(file.name, "wb") as f:
                        for data in file.chunks():
                            f.write(data)
                    ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1), pic2=
                                 uploadFile(pic2), pic3=uploadFile(pic3), pic4=uploadFile(pic4), pic5=uploadFile(
                                 pic5))
        elif pic4:
            os.chdir("home/static/uploads/uploads")
            files = [pic4, pic3, pic2, pic1, pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    with open(file.name, "wb") as f:
                        for data in file.chunks():
                            f.write(data)
                    ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1), pic2=
                                 uploadFile(pic2), pic3=uploadFile(pic3), pic4=uploadFile(pic4))
            os.chdir("../../../..")

        elif pic3:
            os.chdir("home/static/uploads/uploads")
            files = [pic3, pic2, pic1, pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    with open(file.name, "wb") as f:
                        for data in file.chunks():
                            f.write(data)
                    ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1), pic2=
                                 uploadFile(pic2), pic3=uploadFile(pic3))
            os.chdir("../../../..")

        elif pic2:
            print("pic2")
            os.chdir("home/static/uploads/uploads")
            files = [pic2, pic1, pic]
            for file in files:
                if file is not None:
                    print(file)
                    if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                        with open(file.name, "wb") as f:
                            for data in file.chunks():
                                f.write(data)
                        ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1), pic2=
                                 uploadFile(pic2))
            os.chdir("../../../..")

        elif pic1:
            os.chdir("home/static/uploads/uploads")
            files = [pic1, pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    with open(file.name, "wb") as f:
                        for data in file.chunks():
                            f.write(data)
                    ffmpeg(file)

            Posts.objects.update(id=id, content=content, pic=uploadFile(pic), pic1=uploadFile(pic1))
            os.chdir("../../../..")

        elif pic:
            os.chdir("home/static/uploads/uploads")
            files = [pic]
            for file in files:
                if file.name.endswith("mp4") or file.name.endswith("avi") or file.name.endswith("mkv"):
                    ffmpeg(file)
            Posts.objects.filter(id=id).update(content=content, pic=uploadFile(pic))
            os.chdir("../../../..")
        else:
            Posts.objects.filter(id=id).update(content=content)
        return redirect("/")
    else:
        post = Posts.objects.get(id=id)
        return render(request, "home/postupdate.html", {"post": post})


def postInfo(request, post):
    likes = Like.objects.filter(post=post).count()
    comments = Comment.objects.filter(post=post).count()
    try:
        Like.objects.get(user=request.user, post=post)
        res = True
    except Like.DoesNotExist:
        res = False
    return HttpResponse('{} {} Comments {}'.format(likes, comments, res))


def profilePic(request,id):
    import json
    j = serialize("json",Users.objects.filter(user=id))
    return HttpResponse(json.loads(json.dumps(j)),content_type="application/json")


def playVideo(request, vid):
    return render(request, "home/video.html", {"source":vid})


def createReport(request):
    if request.method == "POST":
        post = request.POST["post"]
        comment = request.POST.get("comment")
        if post:
            Report.objects.create(user=request.user, post=Posts.objects.get(id=post))
        if comment:
            Report.objects.create(user=request.user, comment=Comment.objects.get(id=comment))
        return redirect("home:home")
    else:
        return redirect("home:home")

