import os
import re
import glob

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Rename Research Center in sidebar
    content = content.replace('>研究 / 展示中心</a>', '>研究中心</a>')
    content = content.replace('>研究展示中心</a>', '>研究中心</a>')
    content = content.replace('<small>研究展示</small>', '<small>研究中心</small>')
    content = content.replace('研究 / 展示中心', '研究中心')
    content = content.replace('研究 / 專題展示中心', '研究中心')

    # 2. Add Friend Function to sidebar
    # Find planet.html link to insert before it
    content = re.sub(r'(<a\s+[^>]*href="planet\.html"[^>]*>自律星球</a>)', r'<a href="friend.html">好友功能</a>\n          \1', content)
    # Fix if we accidentally added it multiple times (idempotency)
    content = re.sub(r'(<a href="friend\.html">好友功能</a>\n\s*)+', r'<a href="friend.html">好友功能</a>\n          ', content)

    # 3. Rename planet-events.html to planet-friend-visits.html
    content = content.replace('planet-events.html', 'planet-friend-visits.html')

    # 4. In planet.html (or wherever it exists), remove planet-builder.html links
    content = re.sub(r'<a\s+[^>]*href="planet-builder\.html"[^>]*>星球規劃</a>', '', content)
    content = re.sub(r'<a class="hub-card" href="planet-builder\.html">.*?</a>', '', content, flags=re.DOTALL)

    # 5. In index.html, remove personal-template.html and planet-builder.html tool cards
    content = re.sub(r'<a class="tool-launch-card" href="personal-template\.html">.*?</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a class="tool-launch-card" href="planet-builder\.html">.*?</a>', '', content, flags=re.DOTALL)

    # 6. Change "星球事件與好友拜訪" to "好友參訪記錄"
    content = content.replace('星球事件與好友拜訪', '好友參訪記錄')
    content = content.replace('星球事件', '好友參訪記錄')
    content = content.replace('聊天室事件', '聊天室紀錄')
    
    # Specific replacement for the hub card title in planet.html
    content = re.sub(r'<span>✦</span><strong>好友參訪記錄.*?</strong>', r'<span>✦</span><strong>好友參訪記錄</strong>', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for f in glob.glob('web_dashboard/*.html'):
        process_file(f)
    print("HTML files updated successfully.")

if __name__ == '__main__':
    main()
