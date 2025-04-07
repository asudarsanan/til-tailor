import os
import markdown
from jinja2 import Environment, FileSystemLoader
import shutil
from datetime import datetime

# Config
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"
STATIC_DIR = "static"

# Jinja2 setup
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def parse_markdown(file_path: str) -> dict:
    """Parse Markdown files into HTML and metadata."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract metadata (e.g., filename as title/date)
    filename = os.path.basename(file_path)
    slug, _ = os.path.splitext(filename)
    date_str = slug.split("-")[:3]
    date = "-".join(date_str)
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(content)
    
    return {
        "title": slug.replace("-", " ").title(),
        "date": date,
        "slug": slug,
        "html_content": html_content
    }

def generate_site():
    # Clear output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Copy static files
    shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, "static"))
    
    # Process posts
    posts = []
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith(".md"):
            post = parse_markdown(os.path.join(CONTENT_DIR, filename))
            posts.append(post)
            
            # Render individual post
            template = env.get_template("post.html")
            output_html = template.render(post=post)
            output_path = os.path.join(OUTPUT_DIR, f"{post['slug']}.html")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_html)
    
    # Render index page
    posts_sorted = sorted(posts, key=lambda x: x["date"], reverse=True)
    template = env.get_template("index.html")
    index_html = template.render(posts=posts_sorted)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

if __name__ == "__main__":
    generate_site()