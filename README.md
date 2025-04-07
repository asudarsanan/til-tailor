
# TIL Tailor


A minimal static website generator for hosting "Today I Learned" (TIL) posts from Markdown files. Built with Python and Jinja2 templates.

## Features ✨
- 📝 Convert Markdown files to HTML pages
- 📅 Auto-generated index of posts with dates
- 🔄 Live-reload development server
- ✅ PEP8-compliant code with quality checks
- 🚀 One-command build & deployment
- 📱 Responsive HTML templates

## Installation 📦

```bash
git clone https://github.com/asudarsanan/til-tailor.git
cd til-tailor
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
# .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Usage 🛠️

### Create a new post
```bash
echo "## Today I Learned...\nHello World!" > content/$(date +"%Y-%m-%d")-my-post.md
```

### Build the site
```bash
make build  # Outputs to ./output
```

### Run development server
```bash
make serve  # http://localhost:8000
```

### Auto-rebuild on changes
```bash
make watch  # In separate terminal
```

## Project Structure 📂
```
til-generator/
├── content/               # Markdown posts
├── templates/             # Jinja2 templates
│   ├── base.html          # Main layout
│   ├── index.html         # Homepage template
│   └── post.html          # Post template
├── static/                # CSS/JS assets
├── output/                # Generated HTML
├── generator.py           # Build script
├── server.py              # Development server
├── Makefile               # Automation commands
└── requirements.txt       # Python dependencies
```

## Customization 🎨

### 1. Styling
Edit `static/style.css`:
```css
/* Example CSS */
body { font-family: sans-serif; max-width: 800px; margin: 0 auto; }
```

### 2. Templates
Modify files in `templates/`:
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
  <title>TIL | {{ title }}</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
```

### 3. Post Metadata
Add front matter to Markdown files:
```markdown
---
title: "Python Tips"
date: 2024-03-15
tags: python
---
## Today I Learned...
```

## Deployment 🚀

Host the `output/` directory on:
- [GitHub Pages](https://pages.github.com)
- [Netlify](https://netlify.com)
- [Vercel](https://vercel.com)

**Netlify Example**:
1. Drag & drop `output/` folder to Netlify
2. Set build command: `make build`
3. Set publish directory: `output`

## Contributing 🤝

1. Fork the repository
2. Create feature branch:
```bash
git checkout -b feature/improvement
```
3. Commit changes:
```bash
git commit -am 'Add some feature'
```
4. Push to branch:
```bash
git push origin feature/improvement
```
5. Open Pull Request

## Development Setup 💻

```bash
# Install linting tools
pip install flake8 pylint

# Run code checks
make lint

# Test production build
make clean && make build
```

## License 📄
TBD