import os
import re

# 1. Update planet.html
planet_path = 'web_dashboard/planet.html'
with open(planet_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove subnav from planet
content = re.sub(r'<div class="subnav">.*?</div>', '', content, flags=re.DOTALL)
# Remove bottom center-hub page-section completely
content = re.sub(r'<section class="center-hub page-section">.*?</section>', '', content, flags=re.DOTALL)
# Change the subtitle of planet
content = content.replace('星球中心只展示世界，星球、事件、好友拜訪分頁管理。', '只展示自律星球，將你的努力轉為動態宇宙。')
content = content.replace('讓自律星球不只是儀表板，而是可以規劃、解鎖、產生事件的延伸系統。', '看著你的行星系逐漸繁榮，享受自律的成就感。')

with open(planet_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update friend.html
friend_path = 'web_dashboard/friend.html'
with open(friend_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the subnav in friend.html
new_subnav = '''<div class="subnav">
              <a class="active" href="friend.html">好友列表與動態</a>
              <a href="friend-visits.html">好友參訪記錄</a>
              <a href="planet.html">返回我的星球</a>
            </div>'''
content = re.sub(r'<div class="subnav">.*?</div>', new_subnav, content, flags=re.DOTALL)
with open(friend_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Update friend-visits.html
visits_path = 'web_dashboard/friend-visits.html'
with open(visits_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the body data-page
content = content.replace('data-page="planet"', 'data-page="friend"')
# Fix the sidebar active state
content = content.replace('<a class="active" href="planet.html">自律城市 / 星球</a>', '<a href="planet.html">自律城市 / 星球</a>')
content = content.replace('<a href="friend.html">好友功能</a>', '<a class="active" href="friend.html">好友功能</a>')
content = content.replace('<small>城市事件</small>', '<small>好友互動</small>')
# Replace hero header completely to match friend context
new_hero = '''<header class="hero split"><div><span class="eyebrow">Friend Visits</span><h1>好友參訪與互動紀錄。</h1><p>查看好友們什麼時候來拜訪你的星球，以及留下來的鼓勵與互動。</p><div class="subnav">
              <a href="friend.html">好友列表與動態</a>
              <a class="active" href="friend-visits.html">好友參訪記錄</a>
              <a href="planet.html">返回我的星球</a>
            </div></div><div class="hero-card"><span>今日互動</span><strong data-count="8">0</strong><p>好友拜訪 2 次。</p></div></header>'''
content = re.sub(r'<header class="hero split">.*?</header>', new_hero, content, flags=re.DOTALL)

with open(visits_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML pages updated.")
