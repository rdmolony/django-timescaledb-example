from django.shortcuts import render
from django.http import HttpResponse

from .forms import FileForm


def upload_file(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("File upload was successful")
        else:
            return HttpResponse("File upload failed")
    else:
        form = FileForm()
    return render(request, "upload_file.html", {"form": form})
