from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake


class GTestConan(ConanFile):
    name = "gtest"
    version = "master"
    ZIP_FOLDER_NAME = "googletest-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url="http://github.com/smspillaz/conan-gtest"
    license="https://github.com/google/googletest/blob/master/googletest/LICENSE"
    exports = ["CMakeLists.txt"]

    def source(self):
        zip_name = "gtest-%s.zip" % self.version
        url = "https://github.com/google/googletest/archive/master.zip"
        download(url, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        try:
            os.makedirs("_build")
        except OSError:
            pass

        cd_build = "cd _build"
        force = "-Dgtest_force_shared_crt=ON"
        shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        self.run('%s && cmake .. %s %s %s' % (cd_build, cmake.command_line, shared, force))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):
        # Copying headers
        self.copy(pattern="*.h", dst="include", src="%s/googlemock/include" % self.ZIP_FOLDER_NAME, keep_path=True)
        self.copy(pattern="*.h", dst="include", src="%s/googletest/include" % self.ZIP_FOLDER_NAME, keep_path=True)

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=".", keep_path=False)      

    def package_info(self):
        self.cpp_info.libs = ['gtest', 'gtest_main', 'gmock', 'gmock_main']
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        
        if self.options.shared:
            self.cpp_info.defines.append("GTEST_LINKED_AS_SHARED_LIBRARY=1")
