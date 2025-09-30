import sys
from dump_files import move_and_update_all_files
from generate_page import generate_pages_recursively


def main():
    dir_to_build = "docs"
    move_and_update_all_files("static", dir_to_build)
    # generate_page("content/index.md", "template.html", "public/index.html")
    if len(sys.argv) >= 2:
        base_path = sys.argv[1]
        generate_pages_recursively("content", "template.html", dir_to_build, base_path)
    else:
        generate_pages_recursively("content", "template.html", dir_to_build)


main()
