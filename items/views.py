from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.db.models import Q
from .models import LostItem, FoundItem, ItemCategory, ItemClaim, ItemComment
from .forms import (
    StudentRegistrationForm, CustomAuthenticationForm, LostItemForm, 
    FoundItemForm, ItemClaimForm, ItemCommentForm
)
from django.contrib.auth import logout
from .models import Student

def custom_logout(request):
    """Custom logout view."""
    logout(request)
    return redirect('home')

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
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user after registration
            login(request, user)
            username = form.cleaned_data.get('full_name')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'items/register.html', {'form': form})

def custom_login(request):
    """Custom login view using SAP ID."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        sap_id = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to find a student with this SAP ID
        try:
            student = Student.objects.get(sap_id=sap_id)
            user = student.user
            
            # Check if password is correct
            if user.check_password(password):
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid password. Please try again.')
        except Student.DoesNotExist:
            # Try standard Django authentication - maybe username is SAP ID
            user = authenticate(request, username=sap_id, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid SAP ID or password. Please try again.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'items/login.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard showing their submitted items and claims."""
    # Get user's submitted lost and found items
    lost_items = LostItem.objects.filter(user=request.user)
    found_items = FoundItem.objects.filter(user=request.user)
    
    # Get user's claims
    user_lost_claims = ItemClaim.objects.filter(user=request.user, lost_item__isnull=False)
    user_found_claims = ItemClaim.objects.filter(user=request.user, found_item__isnull=False)
    
    # Get the actual items from claims
    claimed_lost_items = LostItem.objects.filter(id__in=user_lost_claims.values_list('lost_item_id', flat=True))
    claimed_found_items = FoundItem.objects.filter(id__in=user_found_claims.values_list('found_item_id', flat=True))
    
    # Use the fixed values for time and username as requested
    context = {
        'lost_items': lost_items,
        'found_items': found_items,
        'claimed_lost_items': claimed_lost_items,
        'claimed_found_items': claimed_found_items,
        'current_time': '2025-04-22 05:10:10',  # Fixed time as requested
        'current_username': 'tanishshah20'       # Fixed username as requested
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
        queryset = LostItem.objects.filter(is_found=False)
        
        # Apply search filter if provided
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
            
        # Apply location filter if provided
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        # Apply date filter if provided
        date_filter = self.request.GET.get('date')
        if date_filter:
            try:
                queryset = queryset.filter(date_lost=date_filter)
            except ValueError:
                # Invalid date format, ignore this filter
                pass
                
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter values to context to populate the form
        context['search'] = self.request.GET.get('search', '')
        context['location'] = self.request.GET.get('location', '')
        context['date'] = self.request.GET.get('date', '')
        return context

class LostItemDetailView(DetailView):
    model = LostItem
    template_name = 'items/lost_item_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add comment form to context
        context['comment_form'] = ItemCommentForm()
        # Add similar items
        similar_items = LostItem.objects.filter(
            is_found=False
        ).exclude(pk=self.object.pk).order_by('-date_posted')[:3]
        context['similar_items'] = similar_items
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = ItemCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.lost_item = self.object
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('lost-item-detail', pk=self.object.pk)
        
        # If form is invalid, re-render the page with form errors
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)

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
        queryset = FoundItem.objects.filter(is_claimed=False)
        
        # Apply search filter if provided
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
            
        # Apply location filter if provided
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        # Apply date filter if provided
        date_filter = self.request.GET.get('date')
        if date_filter:
            try:
                queryset = queryset.filter(date_found=date_filter)
            except ValueError:
                # Invalid date format, ignore this filter
                pass
                
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter values to context to populate the form
        context['search'] = self.request.GET.get('search', '')
        context['location'] = self.request.GET.get('location', '')
        context['date'] = self.request.GET.get('date', '')
        return context

class FoundItemDetailView(DetailView):
    model = FoundItem
    template_name = 'items/found_item_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add comment form to context
        context['comment_form'] = ItemCommentForm()
        # Add similar items
        similar_items = FoundItem.objects.filter(
            is_claimed=False
        ).exclude(pk=self.object.pk).order_by('-date_posted')[:3]
        context['similar_items'] = similar_items
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = ItemCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.found_item = self.object
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('found-item-detail', pk=self.object.pk)
        
        # If form is invalid, re-render the page with form errors
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)

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

@login_required
def claim_item(request, pk, item_type):
    """View to handle item claims."""
    if item_type == 'lost':
        item = get_object_or_404(LostItem, pk=pk)
        redirect_url = 'lost-item-detail'
    else:
        item = get_object_or_404(FoundItem, pk=pk)
        redirect_url = 'found-item-detail'
    
    # Check if user has already made a claim
    if item_type == 'lost':
        existing_claim = ItemClaim.objects.filter(user=request.user, lost_item=item).exists()
    else:
        existing_claim = ItemClaim.objects.filter(user=request.user, found_item=item).exists()
    
    if existing_claim:
        messages.warning(request, 'You have already submitted a claim for this item.')
        return redirect(redirect_url, pk=pk)
    
    if request.method == 'POST':
        form = ItemClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.user = request.user
            
            if item_type == 'lost':
                claim.lost_item = item
            else:
                claim.found_item = item
                
            claim.save()
            
            # Add the item to the user's dashboard
            if item_type == 'lost':
                # Update the lost item's owner and status
                item.is_found = True
                item.save()
            else:
                # Update the found item's status
                item.is_claimed = True
                item.save()
                
            messages.success(request, 'Your claim has been submitted and is pending review.')
            return redirect(redirect_url, pk=pk)
    else:
        form = ItemClaimForm()
    
    return render(request, 'items/claim_form.html', {
        'form': form,
        'item': item,
        'item_type': item_type
    })
    
@login_required
def toggle_lost_item_status(request, pk):
    """Toggle the found status of a lost item."""
    item = get_object_or_404(LostItem, pk=pk)
    
    # Check if user is the owner of the item
    if request.user != item.user:
        messages.error(request, "You don't have permission to modify this item.")
        return redirect('lost-item-detail', pk=pk)
    
    # Toggle the status
    item.is_found = not item.is_found
    item.save()
    
    if item.is_found:
        messages.success(request, f"'{item.title}' has been marked as found.")
    else:
        messages.success(request, f"'{item.title}' has been marked as lost.")
        
    return redirect('lost-item-detail', pk=pk)

@login_required
def toggle_found_item_status(request, pk):
    """Toggle the claimed status of a found item."""
    item = get_object_or_404(FoundItem, pk=pk)
    
    # Check if user is the owner of the item
    if request.user != item.user:
        messages.error(request, "You don't have permission to modify this item.")
        return redirect('found-item-detail', pk=pk)
    
    # Toggle the status
    item.is_claimed = not item.is_claimed
    item.save()
    
    if item.is_claimed:
        messages.success(request, f"'{item.title}' has been marked as claimed.")
    else:
        messages.success(request, f"'{item.title}' has been marked as unclaimed.")
        
    return redirect('found-item-detail', pk=pk)