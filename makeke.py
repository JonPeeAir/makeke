#!/bin/python3

import glob
import argparse
import os

# Setup argument parser
argParser = argparse.ArgumentParser()
argParser.add_argument(
    "main_file",
    metavar="MAIN_FILE", 
    help="the .cpp file containing the main function"
)

# Define Module Class
class Module:
    def __init__(self, cpp_file: str):
        self.cpp = cpp_file
        self.h = []

    def __eq__(self, other) -> bool:
        return self.cpp == other.cpp
        
    def set_headers(self, h_files: list):
        self.h = h_files
        
    def add_header(self, h_file: str):
        self.h.append(h_file)

    def create_rule(self) -> str:
        rule = f"$(obj_dir){self.cpp[:-4]}.o: {self.cpp[:-4]}.cpp"
        for header in self.h:
            rule += f" {header}"
        rule += "\n\t$(shell [ ! -d $(@D) ] && mkdir -p $(@D))\n"
        rule += f"\t$(CXX) -c $< $(CXXFLAGS) -o $@\n\n"
        return rule


def main():

    # Parse command line arguments into an object
    args = argParser.parse_args()
    
    # Get a list of cpp and h files in current directory
    cpp_files: list = glob.glob("*.cpp")
    h_files: list = glob.glob("*.h")

    # Create modules from those cpp and h files
    modules = create_modules(cpp_files, h_files, args.main_file)

    create_makefile(modules)


def create_modules(cpp_files: list, h_files: list, main_file:str) -> list:
    
    # Create each module with their respective cpp_files
    modules: list = list(map(lambda file: Module(file), cpp_files))

    # Add the respective headers for each module
    for module in modules:
        if module.cpp != main_file:
            
            # Pop the right h_file from h_files list
            module_name: str = module.cpp[:-4]
            file_idx: int = h_files.index(module_name + ".h")
            h_file: str = h_files.pop(file_idx)

            # Put h_file in respective module
            module.add_header(h_file)

    # Leftover headers go to the main module
    modules[modules.index(Module(main_file))].set_headers(h_files)

    return modules


def create_makefile(modules: list) -> None:

    compiler_options  = "# Compiler Options\n"
    compiler_options += "CXX := g++\n"
    compiler_options += "CXXFLAGS := -Wall -std=c++17 -g\n\n"

    file_details  = "# File Details\n"
    file_details += "cpp_files := "
    file_details += " ".join(map(lambda module: module.cpp, modules)) + "\n"
    file_details += "obj_dir := obj_files/\n"
    file_details += "obj_files := $(cpp_files:%.cpp=$(obj_dir)%.o)\n\n"

    target_rule  = "# Target Rule\n"
    target_rule += "ws: $(obj_files)\n"
    target_rule += "\t$(CXX) $(obj_files) -o ws\n\n"

    clean_rule  = ".PHONY: clean\n"
    clean_rule += "clean:\n"
    clean_rule += "\trm -rf $(obj_dir)\n\n"
    
    with open("makefile", "w") as makefile:
        makefile.write(compiler_options)
        makefile.write(file_details)
        makefile.write(target_rule)
        for module in modules:
            makefile.write(module.create_rule());
        makefile.write(clean_rule)
        makefile.close()

    if makefile.closed:
        print("Successfully created makefile")
        print("Running make\n")
        os.system("make")
    
    
if __name__ == "__main__":
    main()

