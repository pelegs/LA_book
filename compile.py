import argparse
import pathlib
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--chapters", "-c", type=str, default="ALL")
parser.add_argument("--sections", "-s", type=str, default="ALL")
args = parser.parse_args()

rootDir = pathlib.Path("./chapters")
chapters_all = sorted(list(rootDir.iterdir()))
book_structure = {
    chapter.name: [
        section.stem
        for section in sorted(list(chapter.iterdir()))
        if section.name != "head.tex"
    ]
    for chapter in chapters_all
}

chapters_to_compile = book_structure
if args.chapters != "ALL":
    chapters_from_args = args.chapters.split(",")
    chapters_to_compile = {
        chapter: book_structure[chapter]
        for chapter in chapters_from_args
        if chapter in book_structure.keys()
    }

    if args.sections != "ALL":
        first_chapter_to_compile = chapters_from_args[0]
        sections_in_first_chapter = book_structure[first_chapter_to_compile]
        chapters_to_compile = {
            first_chapter_to_compile: [
                section
                for section in sections_in_first_chapter
                if section in args.sections.split(",")
            ]
        }

print("The following chapters and sections will be compiled:")
for chapter, sections in chapters_to_compile.items():
    print(f"* {chapter}")
    for section in sections:
        print(f" - {section}")
