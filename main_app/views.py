from django.shortcuts import render, redirect # type: ignore
from django.views.generic.edit import CreateView, UpdateView, DeleteView # type: ignore
from django.views.generic import ListView, DetailView # type: ignore
from django.contrib.auth.views import LoginView # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth import login # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.mixins import LoginRequiredMixin # type: ignore
from .models import Cat, Toy # type: ignore
from .forms import FeedingForm


# Create your views here.
class Home(LoginView):
    template_name = 'home.html'
def about(req):
    return render(req, 'about.html')
@login_required
def cats_index(req):
    cats = Cat.objects.filter(user=req.user)
    # You could also retrieve the logged in user's cats like this
    # cats = req.user.cat_set.all()
    return render(req, 'cats/index.html', { 'cats': cats })
def cats_detail(req, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(req, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have
        })
def add_feeding(req, cat_id):
    form = FeedingForm(req.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat_detail', cat_id=cat_id)

def assoc_toy(req, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat_detail', cat_id=cat_id)

def unassoc_toy(req, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('cat_detail', cat_id=cat_id)

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']
class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'
    
class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'
    success_url = '/toys/'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    
class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'
class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'
def signup(req):
    error_message = ''
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('cats_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(req, 'registration/signup.html', context)