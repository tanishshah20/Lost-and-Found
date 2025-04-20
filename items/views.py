from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.db.models import Q
from .models import LostItem, FoundItem, ItemCategory
from .forms import LostItemForm, FoundItemForm, UserRegisterForm

def home(request):
    """Home page view showing recent lost and found items."""
    context = {
        'lost_items': LostItem.objects.filter(is_found=False).order_by('-date_posted')[:5],
        'found_items': FoundItem.objects.filter(is_claimed=False).order_by('-date_posted')[:5],
    }
    return render(request, 'items/home.html', context)

def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'items/register.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard showing their submitted items."""
    lost_items = LostItem.objects.filter(user=request.user)
    found_items = FoundItem.objects.filter(user=request.user)
    context = {
        'lost_items': lost_items,
        'found_items': found_items,
    }
    return render(request, 'items/dashboard.html', context)

def search_items(request):
    """Search functionality for lost and found items."""
    query = request.GET.get('q', '')
    
    if query:
        lost_results = LostItem.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
        
        found_results = FoundItem.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        lost_results = LostItem.objects.none()
        found_results = FoundItem.objects.none()
        
    context = {
        'query': query,
        'lost_results': lost_results,
        'found_results': found_results,
    }
    
    return render(request, 'items/search_results.html', context)

# Lost Item Views
class LostItemListView(ListView):
    model = LostItem
    template_name = 'items/lost_items.html'
    context_object_name = 'items'
    paginate_by = 10
    
    def get_queryset(self):
        return LostItem.objects.filter(is_found=False)

class LostItemDetailView(DetailView):
    model = LostItem
    template_name = 'items/lost_item_detail.html'

class LostItemCreateView(LoginRequiredMixin, CreateView):
    model = LostItem
    form_class = LostItemForm
    template_name = 'items/lost_item_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LostItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LostItem
    form_class = LostItemForm
    template_name = 'items/lost_item_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user

class LostItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LostItem
    template_name = 'items/lost_item_confirm_delete.html'
    success_url = '/lost/'
    
    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user

# Found Item Views
class FoundItemListView(ListView):
    model = FoundItem
    template_name = 'items/found_items.html'
    context_object_name = 'items'
    paginate_by = 10
    
    def get_queryset(self):
        return FoundItem.objects.filter(is_claimed=False)

class FoundItemDetailView(DetailView):
    model = FoundItem
    template_name = 'items/found_item_detail.html'

class FoundItemCreateView(LoginRequiredMixin, CreateView):
    model = FoundItem
    form_class = FoundItemForm
    template_name = 'items/found_item_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FoundItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FoundItem
    form_class = FoundItemForm
    template_name = 'items/found_item_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user

class FoundItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FoundItem
    template_name = 'items/found_item_confirm_delete.html'
    success_url = '/found/'
    
    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user