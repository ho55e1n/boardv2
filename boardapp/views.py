from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MediaForm, dropDownForm, AlbumForm
from .models import Album, UserProfile
from .models import Media


# Create your views here.
def index(request):
    count = Album.objects.all().count()
    myMedia = Media.objects.all()
    mediaPaths = []
    for item in mediaPaths:
        mediaPaths += item.content.path

    context = {'AlbumCount': count, 'mediaList': myMedia, 'mediaPaths': mediaPaths}

    return render(request, 'base.html', context)


def upload_media(request):
    print 'inside upload_media'
    if request.method == 'POST':
        print "request files"
        print request.FILES
        print "request post "
        print request.POST
        form = MediaForm(request.POST, request.FILES)

        if form.is_valid():
            print"iside form is valid"
            media = form.save(commit=False)
            print media
            extension = request.FILES['content'].content_type.split('/')[1]
            if ('mp4' or 'MP4') in extension:
                media.type = 'vid'
            else:
                media.type = 'img'
            media.order = 1
            media.active = True
            media.user = request.user
            destination = Album.objects.filter(id=request.user.currentAlbum).first()
            media.album = destination
            media = form.save()

    else:
        form = MediaForm()

    return render(request, "upload_media.html", locals())


def upload_album(request):
    if request.user.is_authenticated():
        if request.user.albums.all() is not None:
            albums = request.user.albums.all()
    dropdownAlbum = request.POST.get('Albums')
    print 'dropdownAlbum:'
    print dropdownAlbum

    if request.method == 'GET':
        print 'inside GET'
        print request.GET
        album = AlbumForm()
        form = dropDownForm(request.user)
    if ((request.method == 'POST') and ('ExistingAlbum' in request.POST)):
        print 'inside POST'
        print request.POST
        form = dropDownForm(request.user)
        print 'dropdownAlbum'
        print dropdownAlbum
        userID = request.user.id
        print 'userID'
        print userID
        curr = UserProfile.objects.filter(id=userID).first()
        curr.currentAlbum = int(dropdownAlbum)
        intAlbum = int(dropdownAlbum)
        print 'intAlbum'
        print intAlbum
        curr.save()
        # upload_media(request.POST, selectedAlbum)
        return HttpResponseRedirect('/upload-media')

    if ((request.method == 'POST') and ('CreateNewAlbum' in request.POST)):
        form2 = AlbumForm(request.POST)
        if form2.is_valid():
            album = form2.save(commit=False)
            album.user = request.user
            album = form2.save()
            created_album_id = Album.objects.filter(title=album).first().id
            userID = request.user.id
            curr = UserProfile.objects.filter(id=userID).first()
            curr.currentAlbum = created_album_id
            curr.save()
            request.user.albums.add(album)
            return HttpResponseRedirect('/upload-media/')

    return render(request, "base.html", locals())
    '''
    if "CreateNewAlbum" in request.POST:
        if request.method == 'POST':
            form = AlbumForm(request.POST)
            if form.is_valid():
                print "form posted and is valid"
                album = form.save(commit=False)
                album.user = request.user
                print "album user : "
                print album.user
                album = form.save()
                print "outside for.save"
                print "created album id : "
                created_album_id = Album.objects.filter(title=album).first().id
                print "Album id : "
                print created_album_id
                userID = request.user.id
                print "user id"
                print userID
                curr = UserProfile.objects.filter(id=userID).first()
                curr.currentAlbum = created_album_id
                curr.save()
                print "user current album"
                print album.user.currentAlbum
                request.user.albums.add(album)
                return HttpResponseRedirect('/upload-media/')
        else:
            album = AlbumForm()
    return render(request, "base.html", locals())

    if "ExistingAlbum" in request.POST:
        count = Album.objects.all().count()
        myMedia = Media.objects.all()
        if request.user.is_authenticated():
            if request.user.albums.all() is not None:
                albums = request.user.albums.all()

        dropdownAlbum = request.POST.get('Albums')
        print 'dropdownAlbum:'
        print dropdownAlbum
        if request.method == 'GET':
            print 'inside GET'
            print request.GET
            form2 = dropDownForm(request.user)
        else:
            print 'inside POST'
            print request.POST
            form2 = dropDownForm(request.user)
            print 'dropdownAlbum'
            print dropdownAlbum
            userID = request.user.id
            print 'userID'
            print userID
            curr = UserProfile.objects.filter(id=userID).first()
            curr.currentAlbum = int(dropdownAlbum)
            intAlbum = int(dropdownAlbum)
            print 'intAlbum'
            print intAlbum
            curr.save()
            # upload_media(request.POST, selectedAlbum)
            return HttpResponseRedirect('/upload-media')
    return render(request, "base.html", locals())
'''
# return HttpResponseRedirect('/upload-media')


def sort(request):
    """
    List all medias sorted by active/inactive in sortable lists
    media() has a required boolean field named 'active'
    """
    print request.POST
    print 'inside sort view'
    lastAlbumID = request.user.currentAlbum
    print lastAlbumID
    print type(lastAlbumID)
    lastAlbum = Album.objects.filter(id=lastAlbumID).first()
    media_list = Media.objects.filter(album=lastAlbum)
    active = []
    inactive = []

    for media in media_list:
        if media.active:
            active.append(media)
        else:
            inactive.append(media)

    if request.method == "POST":
        def id_cleaner(id_list):
            clean_id_list = []
            for item in id_list:
                try:
                    clean_id_list.append(int(item))
                except ValueError:
                    pass
            return clean_id_list

        def update_medias(id_list, active, trash=False):
            clean_ids = id_cleaner(id_list)
            sorting_counter = 0
            for i in clean_ids:
                if trash:
                    # While this is fine for my requirements, you may want
                    # to check permissions here (I have @login_required)
                    m = Media.objects.filter(id=i).first()
                    m.order = sorting_counter
                    m.active = active
                    print "media id : "
                    print m.id
                    print "order value  : "
                    print m.order
                    sorting_counter += 1
                    m.save()



        if 'active' in request.POST:
            active_list = request.POST.getlist('image[]')
            print 'active found'
            print "\n"
            print active_list
            update_medias(active_list, active=True)

        if 'inactive' in request.POST:
            inactive_list = request.POST.getlist('image[]')
            print 'inactive found'
            print "\n"
            print inactive_list
            update_medias(inactive_list, active=False)

        if 'trash' in request.POST:
            trash_list = request.POST.getlist('image[]')
            print 'trash found'
            print "\n"
            print trash_list
            print "inside trash request post :"
            update_medias(trash_list, active=False, trash=True)

    context_dict = {'video': inactive,
                    'images': active}
    return render(request, "sort.html", context_dict)
