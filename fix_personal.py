import os
import re
import glob

# The unified subnav for all personal pages
unified_subnav = '''<div class="subnav" style="margin-bottom: 24px;">
              <a href="personal.html">中心總覽</a>
              <a href="personal-trends.html">趨勢</a>
              <a href="personal-pressure.html">壓力雷達</a>
              <a href="personal-weather.html">自律天氣</a>
              <a href="personal-time-capsule.html">時間膠囊</a>
              <a href="personal-letter.html">未來的信</a>
              <a href="personal-skill-tree.html">人生技能樹</a>
            </div>'''

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Rename "技能樹" to "人生技能樹" globally in text
    content = content.replace('技能樹', '人生技能樹')
    content = content.replace('人生人生技能樹', '人生技能樹') # Prevent double replacing

    # 2. Find which page this is to set the active class
    filename = os.path.basename(path)
    active_href = f'href="{filename}"'
    page_subnav = unified_subnav.replace(active_href, f'class="active" {active_href}')

    if filename == 'personal.html':
        # For the hub page, maybe keep the hero, but still update the subnav
        content = re.sub(r'<div class="subnav">.*?</div>', page_subnav.replace('style="margin-bottom: 24px;"', ''), content, flags=re.DOTALL)
    else:
        # For the sub-pages, remove the hero header and replace with just the subnav
        # Wait, if we completely remove <header class="hero split">, we should replace it with the subnav
        # We find <header ...>...</header> and replace it with <header class="page-section" style="padding-bottom: 0;"> + subnav + </header>
        if '<header class="hero split">' in content:
            replacement = f'<div class="page-section" style="padding-bottom: 0; padding-top: 20px;">{page_subnav}</div>'
            content = re.sub(r'<header class="hero split">.*?</header>', replacement, content, flags=re.DOTALL)
        else:
            # If it was already replaced or different format, just ensure subnav is updated
            content = re.sub(r'<div class="subnav".*?</div>', page_subnav, content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('web_dashboard/personal*.html'):
    process_file(f)

print("Personal pages updated.")
