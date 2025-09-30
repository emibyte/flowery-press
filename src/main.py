from dump_files import move_and_update_all_files
from generate_page import generate_pages_recursively


def main():
    move_and_update_all_files("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursively("content", "template.html", "public")


main()
