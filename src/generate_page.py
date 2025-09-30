import os
from markdown_parsing import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:]
    raise Exception("no h1 header found in markdown")


def generate_page(
    from_path: str, template_path: str, dest_path: str, base_path: str = "/"
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_contents = ""
    final_html = ""
    with open(from_path, mode="r") as f:
        markdown_contents = f.read()
    with open(template_path, mode="r") as f:
        final_html = f.read()

    html = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)

    final_html = (
        final_html.replace("{{ Content }}", html)
        .replace("{{ Title }}", title)
        .replace('href="/', f'href="{base_path}')
        .replace('src="/', f'src="{base_path}')
    )

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(dest_path, mode="w") as f:
        f.write(final_html)
    return


def generate_pages_recursively(
    dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str = "/"
) -> None:
    for file in os.listdir(dir_path_content):
        source_file_path = os.path.join(dir_path_content, file)
        dest_file_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(source_file_path):
            dest_file_path = dest_file_path.replace(".md", ".html")
            generate_page(source_file_path, template_path, dest_file_path)
        else:
            generate_pages_recursively(source_file_path, template_path, dest_file_path)
    return
