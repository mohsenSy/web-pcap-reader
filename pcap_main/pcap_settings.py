import os
import six.moves.configparser

from django.conf import settings

config = six.moves.configparser.RawConfigParser()

KNOWN_SECTIONS = ["pcap"]

config.read(os.path.join(settings.BASE_DIR, "conf/pcap.conf"))

def get_option(section, option):
    if config.has_section(section):
        return config.get(section, option)
    return None

def set_option(section, option):
    config.set(section, option)

def save_config():
    config.write(open(os.path.join(settings.BASE_DIR, "conf/pcap.conf"), "w"))

def get_all_settings():
    all_settings = []
    for section in KNOWN_SECTIONS:
        items = config.items(section)
        all_settings.extend(items)
    return all_settings
