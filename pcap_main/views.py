from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from . import pcap_analyse
from . import pcap_settings
from .forms import EditSettingsForm


import os

# Create your views here.

def home(request):
    return render(request, 'pcap_main/home.html')

def read(request):
    try:
        listing = os.listdir(pcap_settings.get_option("pcap", "pcap_dir"))
    except OSError as e:
        return render(request, 'pcap_main/read.html')
    files = []
    for l in listing:
        if os.path.isfile(pcap_settings.get_option("pcap", "pcap_dir") + "/" + l):
            files.append(l)

    return render(request, 'pcap_main/read.html', {'files': files})

def readfile(request, filename):
    filepath = pcap_settings.get_option("pcap", "pcap_dir") + "/" + filename
    if not os.path.isfile(filepath):
        return render(request, "pcap_main/file_not_found.html", {"filename": filename})

    pcap = pcap_analyse.pcap_reader(filepath)
    try:
        packets = pcap.read_packets()
    except ValueError as e:
        return render(request, "pcap_main/file_invalid.html", {"filename": filename})

    page = request.GET.get('page', 1)
    count = len(packets)
    paginator = Paginator(packets, 15)
    try:
        packet_list = paginator.page(page)
    except PageNotAnInteger:
        packet_list = paginator.page(1)
    except EmptyPage:
        packet_list = paginator.page(paginator.num_pages)

    context = {
        "filename": filename,
        "count": count,
        "packets": packet_list
    }
    return render(request, "pcap_main/read_file.html", context)
