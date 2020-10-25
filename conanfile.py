from conans import ConanFile, CMake

class StringChallenge(ConanFile):
    name = 'Challenge_Template'
    version = '0.1'
    settings = 'os', 'arch', 'compiler', 'build_type'
    requires = "gtest/1.8.1@bincrafters/stable", "benchmark/1.5.0"
    generators = "cmake_find_package" # can be updated to cmake_find_package_multi if necessary
    exports = ["LICENSE.md"]
    exports_sources = ["src/*","CMakeLists.txt"]
    default_options = {"gtest:build_gmock": False}

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "lib")

    def build(self):
        cmake = CMake(self, generator='Ninja')
        cmake.configure()
        cmake.build()
        cmake.test() # If you dont have any tests this will fail!