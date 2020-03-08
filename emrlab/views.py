from django.shortcuts import render
import os

module_dir = os.path.dirname(__file__)  # get current directory
labhome_content = os.path.join(module_dir, 'resources/emrlabhome.md')
lab1_content = os.path.join(module_dir, 'resources/lab1.md')
lab2_content = os.path.join(module_dir, 'resources/lab2.md')
lab3_content = os.path.join(module_dir, 'resources/lab3.md')
lab4_content = os.path.join(module_dir, 'resources/lab4.md')
finish_content = os.path.join(module_dir, 'resources/finishlab.md')

def index(request):
    contents = open(labhome_content, "rt")
    return render(request, 'index.html', {'content': contents.read()})

def lab1(request):
    contents = open(lab1_content, "rt")
    return render(request, 'index.html', {'content': contents.read()})

def lab2(request):
    contents = open(lab2_content, "rt")
    return render(request, 'index.html', {'content': contents.read()})

def lab3(request):
    contents = open(lab3_content, "rt")
    return render(request, 'index.html', {'content': contents.read()})

def lab4(request):
    contents = open(lab4_content, "rt")
    return render(request, 'index.html', {'content': contents.read()})

def finish(request):
    contents = open(finish_content, "rt")
    return render(request, 'index.html', {'content': contents.read()})
