#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy
import json, os

required_conan_version = ">=2.0"

class libxsdConan(ConanFile):
    jsonInfo = json.load(open("info.json", 'r'))
    # ---Package reference---
    name = jsonInfo["projectName"]
    version = jsonInfo["version"]
    user = jsonInfo["domain"]
    channel = "stable"
    # ---Metadata---
    description = jsonInfo["projectDescription"]
    license = jsonInfo["license"]
    author = jsonInfo["vendor"]
    topics = jsonInfo["topics"]
    homepage = jsonInfo["homepage"]
    url = jsonInfo["repository"]
    # ---Requirements---
    requires = ["xerces-c/[>=3.2.4]"]
    tool_requires = []
    # ---Sources---
    exports = ["info.json"]
    exports_sources = []
    # ---Binary model---
    settings = "os", "arch"
    options = {}
    default_options = {
        "xerces-c/*:shared": False,
        "xerces-c/*:network": False,
    }
    package_type = "header-library"
    no_copy_source = True

    def validate(self):
        valid_os = ["Windows", "Linux", "Macos"]
        if str(self.settings_build.os) not in valid_os:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following operating systems: {valid_os}")
        valid_arch = ["x86_64", "armv8"]
        if str(self.settings_build.arch) not in valid_arch:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following architectures on {self.settings.os}: {valid_arch}")

    def source(self):
        get(self, **self.conan_data["sources"][self.version]["libXSD"], strip_root=True)

    def build(self):
        get(self, **self.conan_data["sources"][self.version][str(self.settings_build.os)][str(self.settings_build.arch)], strip_root=True)

    def package(self):
        copy(self, "*", os.path.join(self.source_folder, "xsd"), os.path.join(self.package_folder, "include", "xsd"))
        copy(self, "usr/local/bin/xsd", os.path.join(self.build_folder), os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, "bin/xsd.exe", os.path.join(self.build_folder), os.path.join(self.package_folder, "bin"), keep_path=False)

    def package_id(self):
        self.info.settings_build = self.settings_build

    def package_info(self):
        self.output.info('Prepending to PATH environment variable: %s' % os.path.join(self.package_folder, "bin"))
        self.buildenv_info.prepend_path("PATH", os.path.join(self.package_folder, "bin"))
        self.cpp_info.libdirs = []
