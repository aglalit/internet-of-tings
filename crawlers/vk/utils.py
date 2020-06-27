#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import glob
import datetime
import json

import base64
import requests
import socket
import wget

import vkapi


def remove_symbols(filename):
    if len(filename) >=128:
        return re.sub(r'[\\\\/:*?\"<>|\n\r\xa0]', "", filename[0:126])
    else:
        return re.sub(r'[\\\\/:*?\"<>|\n\r\xa0]', "", filename)


def file_exists(path):
    try:
        return os.path.exists(path)
    except OSError:
        return False


def get_path(self, flags, Object):
    if flags:
        path = Object.getExistingDirectory(self, "Выберите папку для скачивания", "", Object.ShowDirsOnly)
        if path == "":
            return os.getcwd()
        else:
            return path
    else:
        return os.getcwd()


def remove_files(paths, pattern):
    files = glob.glob(paths + "/" + pattern)
    
    if not files:
        return True

    for file in files:
        try:
            os.remove(file)
        except:
            continue


def get_proxy_host(flags, api=True):
    if flags:
        if api:
            return vkapi.BASE_PROXY_API_URL
        else:
            return vkapi.BASE_PROXY_OAUTH_URL
    else:
        if api:
            return vkapi.BASE_API_URL
        else:
            return vkapi.BASE_OAUTH_URL  



def check_connection(url):
    try:
        requests.get(url, timeout=5)
    except Exception:
        return False

    return True


def get_internal_ip():
    try:
        return socket.gethostbyname(socket.getfqdn())
    except Exception:
        return None


def get_external_ip():
    try:
        return bytes(requests.get("http://ident.me/", timeout=5).content
            ).decode("utf-8")

    except Exception:
        return None


def get_network_info():
    return requests.get("http://ipinfo.io", timeout=5).json()


def unix_time_stamp_convert(time):
    return datetime.datetime.fromtimestamp(int(time)
        ).strftime("%d.%m.%Y %H:%M:%S")


def time_duration(time):
    return str(datetime.timedelta(seconds=int(time)))


def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


def downloads_files_in_wget(url, filename, progress=""):
    wget.download(url, filename, bar=progress)
