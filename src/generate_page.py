import os
from markdown_parsing import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:]
    raise Exception("no h1 header found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_contents = ""
    template = ""
    with open(from_path, mode="r") as f:
        markdown_contents = f.read()
    with open(template_path, mode="r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)

    template = template.replace("{{ Content }}", html).replace("{{ Title }}", title)

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(dest_path, mode="w") as f:
        f.write(template)
    return
