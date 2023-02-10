from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
import zipfile
import mimetypes
import os


class DownloadView(View):
    def get(self, request, pk):
        folder = Folder.objects.get(pk=pk)
        files = folder.file_set.all()
        request.session['folder'] = str(folder.uuid)
        return render(request, template_name="main/download.html", context={"files": files,
                                                                            "title": "Download",
                                                                            "folder": folder})  # For guessing
        # file's type make template_tag!


class DownloadConfirmedAPIView(APIView):
    def post(self, request):
        folder_pk = request.session['folder']
        del request.session['folder']
        folder = Folder.objects.get(pk=folder_pk)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder_name = str(folder.folder_name)
        folder_path = base_dir + "/" + folder_name + ".zip"
        path = open(folder_path, 'rb')
        mime_type, _ = mimetypes.guess_type(folder_path)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % folder_path
        return response


def upload(request):
    folder = request.session.get('folder', None)
    context = {}
    try:
        context = {'download_link': "127.0.0.1:8000/download/" + folder['uuid']}
        del request.session['folder']
    except :
        pass
    print(context)
    return render(request, template_name='main/main.html', context=context)


class HandleApiView(APIView):
    def post(self, request):
        folder_name = request.data.get('folder')
        if folder_name:
            folder = Folder.objects.create(folder_name=folder_name)
        else:
            folder = Folder.objects.create()
        model_sr = FileListSerializer(data=request.data)
        if model_sr.is_valid(raise_exception=True):
            model_sr.save(folder=folder)
            model_sr.zip_files(folder)
            request.session['folder'] = FolderSerializer(folder).data
            return redirect('upload')
        return Response({'status_code': 400})

    def get(self, request):
        folders = Folder.objects.all()
        folder_serializer = FolderSerializer(folders, many=True)
        files = File.objects.all()
        files_serializer = FileSerializer(files, many=True)
        if 'uuid' in request.session:
            del request.session['uuid']
        return Response({"data": folder_serializer.data,
                         "Files": files_serializer.data})
