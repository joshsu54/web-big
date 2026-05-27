import os
import re
import glob

unified_subnav = '''<div class="subnav" style="margin-bottom: 24px;">
              <a href="research.html">中心總覽</a>
              <a href="research-scenario.html">Demo 場景</a>
              <a href="research-anonymized.html">匿名資料</a>
              <a href="research-score-demo.html">分數展示</a>
            </div>'''

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(path)
    active_href = f'href="{filename}"'
    page_subnav = unified_subnav.replace(active_href, f'class="active" {active_href}')

    if filename == 'research.html':
        content = re.sub(r'<div class="subnav">.*?</div>', page_subnav.replace('style="margin-bottom: 24px;"', ''), content, flags=re.DOTALL)
    else:
        if '<header class="hero split">' in content:
            replacement = f'<div class="page-section" style="padding-bottom: 0; padding-top: 20px;">{page_subnav}</div>'
            content = re.sub(r'<header class="hero split">.*?</header>', replacement, content, flags=re.DOTALL)
        else:
            content = re.sub(r'<div class="subnav".*?</div>', page_subnav, content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('web_dashboard/research*.html'):
    process_file(f)

print("Research pages updated.")
