from django.shortcuts import render
from django.http import HttpResponse

from .forms import FileForm
from .forms import FileTypeForm


def create_file_type(request):
    if request.method == "POST":
        form = FileTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("File type was created")
        else:
            return HttpResponse(f"File type creation failed: {form.errors}")
    else:
        form = FileTypeForm()
    return render(request, "create_file_type.html", {"form": form})


def upload_file(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("File upload was successful")
        else:
            return HttpResponse(f"File type creation failed: {form.errors}")
    else:
        form = FileForm()
    return render(request, "upload_file.html", {"form": form})


def index(request):
    return render(request, "index.html")
