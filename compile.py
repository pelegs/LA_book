import argparse
import copy
import pathlib
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--structure", "-s", type=str, default="ALL")
args = parser.parse_args()

rootDir = pathlib.Path("./chapters")
chapters_all = sorted(list(rootDir.iterdir()))
full_book_structure = {
    chapter.name: [
        section.stem
        for section in sorted(list(chapter.iterdir()))
        if section.name != "head.tex"
    ]
    for chapter in chapters_all
}

structure_to_compile = copy.deepcopy(full_book_structure)
if args.structure != "ALL":
    chapters_list = args.structure.split(";")
    structure_to_compile = {
        chapter_name: [
            section
            for section in chapter.split(":")[1].split(",")
            if section in full_book_structure[chapter_name]
        ]
        for chapter in chapters_list
        if (chapter_name := chapter.split(":")[0]) in full_book_structure.keys()
    }

print("The following chapters and sections will be compiled:")
for chapter, sections in structure_to_compile.items():
    print(f"* {chapter}")
    for section in sections:
        print(f" - {section}")

# file = "main/main"
# job = "wip"
# chapter = "2_theBasics"
# section = "2_linearTrans"
# latexmk_cmd = f'latexmk -pdflua -shell-escape -jobname=main/{job} -pretex="\def\wipchapter{chapter}\def\wipsection{section}" -usepretex {file}'
