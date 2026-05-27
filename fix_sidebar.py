import os
import re
import glob

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add friend.html if not present
    if 'href="friend.html"' not in content:
        # It could be planet.html
        content = re.sub(r'(<a[^>]*href="planet\.html"[^>]*>.*?</a>)', r'<a href="friend.html">好友功能</a>\n          \1', content)

    # Remove groups-templates.html
    content = re.sub(r'<a[^>]*href="groups-templates\.html"[^>]*>.*?</a>', '', content)
    
    # Check for personal-template.html just in case
    content = re.sub(r'<a[^>]*href="personal-template\.html"[^>]*>.*?</a>', '', content)

    # Check for planet-builder.html just in case
    content = re.sub(r'<a[^>]*href="planet-builder\.html"[^>]*>.*?</a>', '', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('web_dashboard/*.html'):
    fix_file(f)

print("Sidebars fixed.")
