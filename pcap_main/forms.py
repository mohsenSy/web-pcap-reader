from django import forms
from django.forms import ValidationError

class EditSettingsForm(forms.Form):
    pcap_dir = forms.CharField(label="PCAP files directory", max_length=100)

    def clean_pcap_dir(self):
        pcap_dir = self.cleaned_data["pcap_dir"]
        if pcap_dir.startswith("/var/") and len(pcap_dir) > 5:
            return pcap_dir
        raise ValidationError("Dir must be a subdirectory of /var/")
