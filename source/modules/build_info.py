import json
import os
import re
import subprocess
import time
from pathlib import Path
from subprocess import DEVNULL

from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import *
from modules.settings import *

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


class BuildInfo:
    def __init__(self, link_type, link, subversion, build_hash, commit_time, branch, size=None):
        self.link_type = link_type
        self.link = link
        self.subversion = subversion
        self.build_hash = build_hash
        self.commit_time = commit_time
        self.branch = branch
        self.size = size

    def __eq__(self, other):
        if (self.build_hash is not None) and (other.build_hash is not None):
            return self.build_hash == other.build_hash
        else:
            return self.get_name() == other.get_name()

    def get_name(self):
        if self.link_type == 'link':
            return Path(self.link).stem
        elif self.link_type == 'path':
            return Path(self.link).name


class BuildInfoReader(QThread):
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, path):
        QThread.__init__(self)
        self.path = path

    def run(self):
        build_info = self.read_build_info(self.path)
        self.finished.emit(build_info)
        return

    def write_build_info(self, folder):
        # Read Blender Version
        platform = get_platform()

        if platform == 'Windows':
            blender_exe = "blender.exe"
        elif platform == 'Linux':
            blender_exe = "blender"

        exe_path = Path(get_library_folder()) / folder / blender_exe

        if platform == 'Windows':
            info = subprocess.check_output(
                [exe_path.as_posix(), "-v"],
                creationflags=CREATE_NO_WINDOW,
                shell=True,
                stderr=DEVNULL, stdin=DEVNULL)
        elif platform == 'Linux':
            info = subprocess.check_output(
                [exe_path.as_posix(), "-v"], shell=False,
                stderr=DEVNULL, stdin=DEVNULL)

        info = info.decode('UTF-8')

        set_locale()
        ctime = re.search("build commit time: " + "(.*)", info)[1].rstrip()
        cdate = re.search("build commit date: " + "(.*)", info)[1].rstrip()
        strptime = time.strptime(cdate + ' ' + ctime, "%Y-%m-%d %H:%M")
        commit_time = time.strftime("%d-%b-%y-%H:%M", strptime)
        build_hash = re.search("build hash: " + "(.*)", info)[1].rstrip()
        subversion = re.search("Blender " + "(.*)", info)[1].rstrip()

        try:
            if platform == 'Windows':
                folder_parts = folder.name.replace(
                    "blender-", "").replace("-windows64", "").rsplit('-', 2)
            elif platform == 'Linux':
                folder_parts = folder.name.replace(
                    "blender-", "").replace("-linux64", "").rsplit('-', 2)

            if len(folder_parts) > 2:
                branch = folder_parts[0]
            elif len(folder_parts) > 1:
                branch = "daily"
            else:
                branch = "stable"
        except Exception as e:
            branch = None

        # Write Version Information
        data = {}
        data['blinfo'] = []
        data['blinfo'].append({
            'branch': branch,
            'subversion': subversion,
            'build_hash': build_hash,
            'commit_time': commit_time,
        })

        path = Path(get_library_folder()) / folder / '.blinfo'

        with open(path, 'w') as file:
            json.dump(data, file)

    def read_build_info(self, folder):
        path = Path(get_library_folder()) / folder / '.blinfo'

        if not path.is_file():
            self.write_build_info(folder)

        with open(path) as file:
            data = json.load(file)
            blinfo = data['blinfo'][0]
            link = Path(get_library_folder()) / folder

            build_info = BuildInfo(
                'path',
                link,
                blinfo['subversion'],
                blinfo['build_hash'],
                blinfo['commit_time'],
                blinfo['branch']
            )

            return build_info
