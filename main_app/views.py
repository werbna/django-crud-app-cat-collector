from django.shortcuts import render, redirect # type: ignore
from django.views.generic.edit import CreateView, UpdateView, DeleteView # type: ignore
from .models import Cat, Toy # type: ignore
from .forms import FeedingForm


# Create your views here.
def home(req):
    return render(req, 'home.html')
def about(req):
    return render(req, 'about.html')
def cats_index(req):
    cats = Cat.objects.all()
    return render(req, 'cats/index.html', {'cats': cats})
def cats_detail(req, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    return render(req, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': feeding_form
        })
def add_feeding(req, cat_id):
    form = FeedingForm(req.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat_detail', cat_id=cat_id)

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']
class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'
    
class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'