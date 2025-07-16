from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm, RegisterForm

def home(request):
    return render(request, 'notepad/home.html')

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('note_list')
    return render(request, 'notepad/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('note_list')
    return render(request, 'notepad/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def note_list(request):
    notes = Note.objects.filter(owner=request.user)
    return render(request, 'notepad/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        note = form.save(commit=False)
        note.owner = request.user
        note.save()
        return redirect('note_list')
    return render(request, 'notepad/note_form.html', {'form': form})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    return render(request, 'notepad/note_detail.html', {'note': note})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('note_detail', pk=note.pk)
    return render(request, 'notepad/note_form.html', {'form':form})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notepad/note_confirm_delete.html', {'note':note})
