"""
Static site generator for TIL-Tailor.
Converts markdown files to HTML and generates a static website.
"""
import os
import shutil
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import markdown


# Config
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"
STATIC_DIR = "static"
TAG_DIR = "tags"  # Directory for tag-specific pages
RECENT_POSTS_COUNT = 5  # Number of recent posts to display

# Jinja2 setup
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def extract_front_matter(content):
    """Extract front matter from markdown content."""
    meta = {}
    front_matter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)

    if front_matter_match:
        front_matter = front_matter_match.group(1)
        content = content[front_matter_match.end():]

        # Parse front matter
        for line in front_matter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip().lower()] = value.strip().strip('"\'')

    return meta, content


def parse_date_from_filename(filename):
    """Extract date from filename pattern YYYY-MM-DD-title."""
    slug, _ = os.path.splitext(filename)
    date_str = slug.split("-")[:3]

    try:
        parsed_date = datetime(
            int(date_str[0]),
            int(date_str[1]),
            int(date_str[2])
        )
        return parsed_date.strftime("%Y-%m-%d"), slug
    except (ValueError, IndexError):
        return "-".join(date_str), slug


def parse_markdown(file_path: str) -> dict:
    """Parse Markdown files into HTML and metadata."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract front matter and content
    meta, content = extract_front_matter(content)

    # Get date and slug from filename
    filename = os.path.basename(file_path)
    date, slug = parse_date_from_filename(filename)

    # Generate HTML and post metadata
    html_content = markdown.markdown(content)
    title = meta.get('title', slug.replace("-", " ").title())

    # Extract tags or use default
    tags = []
    if 'tags' in meta:
        tags = [tag.strip() for tag in meta['tags'].split(',')]

    return {
        "title": title,
        "date": meta.get('date', date),
        "slug": slug,
        "tags": tags,
        "html_content": html_content
    }


def generate_post_page(post, output_dir):
    """Generate a single post page."""
    template = env.get_template("post.html")
    output_html = template.render(post=post, title=post["title"])
    output_path = os.path.join(output_dir, f"{post['slug']}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_html)


def generate_tag_pages(tags_dict, tags_output_dir):
    """Generate pages for each tag."""
    tag_template = env.get_template("tag.html")
    for tag, tag_posts in tags_dict.items():
        tag_html = tag_template.render(
            tag=tag,
            tag_title=tag.title(),
            posts=tag_posts,
            title=f"Tag: {tag}"
        )
        tag_path = os.path.join(tags_output_dir, f"{tag}.html")
        with open(tag_path, "w", encoding="utf-8") as f:
            f.write(tag_html)


def organize_posts_by_tags(posts):
    """Organize posts into tag categories."""
    tags_dict = {}
    for post in posts:
        if not post["tags"]:
            tag = "uncategorized"
            if tag not in tags_dict:
                tags_dict[tag] = []
            tags_dict[tag].append(post)
        else:
            for tag in post["tags"]:
                if tag not in tags_dict:
                    tags_dict[tag] = []
                tags_dict[tag].append(post)
    return tags_dict

def render_index(posts, tags_dict):
    """Render the index page with custom title."""
    # Sort posts by date for recent posts section
    recent_posts = sorted(posts, key=lambda x: x["date"], reverse=True)[:10]
    
    # Pass a custom title for the index page
    index_template = env.get_template("index.html")
    return index_template.render(
        recent_posts=recent_posts, 
        tags_dict=tags_dict, 
        title="Home"
    )

def generate_site():
    """Generate static site from Markdown content."""
    # Setup directories
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Copy static files
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, "static"))
    else:
        os.makedirs(os.path.join(OUTPUT_DIR, "static"), exist_ok=True)

    # Create tags directory
    tags_output_dir = os.path.join(OUTPUT_DIR, TAG_DIR)
    os.makedirs(tags_output_dir, exist_ok=True)

    # Parse markdown files and generate posts
    posts = []
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith(".md"):
            post = parse_markdown(os.path.join(CONTENT_DIR, filename))
            posts.append(post)
            generate_post_page(post, OUTPUT_DIR)

    # Sort and organize posts
    posts_sorted = sorted(posts, key=lambda x: x["date"], reverse=True)
    recent_posts = posts_sorted[:RECENT_POSTS_COUNT]
    tags_dict = organize_posts_by_tags(posts_sorted)

    # Generate tag pages
    generate_tag_pages(tags_dict, tags_output_dir)

    index_html = render_index(posts_sorted, tags_dict)

    output_index = os.path.join(OUTPUT_DIR, "index.html")
    with open(output_index, "w", encoding="utf-8") as f:
        f.write(index_html)


if __name__ == "__main__":
    generate_site()
