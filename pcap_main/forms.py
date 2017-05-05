from django import forms
from django.forms import ValidationError

import os

class EditSettingsForm(forms.Form):
    pcap_dir = forms.CharField(label="PCAP files directory", max_length=100)

    def clean_pcap_dir(self):
        pcap_dir = self.cleaned_data["pcap_dir"]
        if pcap_dir.startswith("/var/") and len(pcap_dir) > 5 and os.path.isdir(pcap_dir):
            return pcap_dir
        raise ValidationError("PCAP Dir must be a subdirectory of /var/ and it must exist")
