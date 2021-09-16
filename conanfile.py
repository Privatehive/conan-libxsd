#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import shutil
import os


class libxsdConan(ConanFile):
    name = "libxsd"
    version = "4.0.0"
    description = "CodeSynthesis XSD is a W3C XML Schema to C++ translator"
    url = "https://github.com/Tereius/conan-libxsd"
    homepage = "https://www.codesynthesis.com/projects/xsd/"
    license = "GPLv2"
    settings = "os", "arch"

    @property
    def arch(self):
        return "x86_64" if self.settings.arch == "x86_64" else "i686"

    def source(self):
        v = tools.Version(self.version)
        if self.settings.os == 'Windows':
            source_url = "https://www.codesynthesis.com/download/xsd/%s.%s/windows/i686/xsd-%s-i686-windows.zip" % (v.major, v.minor, self.version)
        elif self.settings.os == 'Macos':
            source_url = "https://www.codesynthesis.com/download/xsd/%s.%s/macosx/i686/xsd-%s-i686-macosx.tar.bz2" % (v.major, v.minor, self.version)
        else:
            source_url = "https://www.codesynthesis.com/download/xsd/%s.%s/linux-gnu/%s/xsd-%s-%s-linux-gnu.tar.bz2" % (v.major, v.minor, self.arch, self.version, self.arch)
        tools.get(source_url)

    def package(self):

        if self.settings.os == 'Windows':
            folder = "xsd-%s-i686-windows" % self.version
        elif self.settings.os == 'Macos':
            folder = "xsd-%s-i686-macosx" % self.version
        else:
            folder = "xsd-%s-%s-linux-gnu" % (self.version, self.arch)
        self.copy("*", src=folder)
        self.copy("*", src=os.path.join(folder, "libxsd"), dst="include")

    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: %s' % bin_path)
        self.env_info.PATH.append(bin_path)
