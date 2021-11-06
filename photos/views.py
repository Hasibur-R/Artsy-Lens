from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


# Create your views here.

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')



def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)



@login_required(login_url='login')
def gallery(request):
    if 'q' in request.GET:
        q = request.GET['q']
        photos = Photo.objects.filter(photo_title__icontains=q)

    # photos = Photo.objects.all()
        context = {
           'photos': photos
        }
        return render(request, 'photos/search.html', context)
    
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo':photo})


@login_required(login_url='login')
def uploadPhoto(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])

        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])

        else:
            category = None

        
        photo = Photo.objects.create(
           category=category,
           photo_title=data['photo_title'],
           image=image,
           photo_price=data['photo_price'],
           frame_size=data['frame_size']
        )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/upload.html', context)
    
def about(request):
    return render(request, 'photos/about.html')