import os
import re

app_js_path = 'web_dashboard/assets/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update the modules array in app.js
new_modules = '''const modules = [
  ["home", "總覽入口", "index.html"],
  ["personal", "個人進階分析", "personal.html"],
  ["guardian", "家長陪伴中心", "guardian.html"],
  ["groups", "團體 / 教育管理", "groups.html"],
  ["operations", "商城頁", "operations.html"],
  ["research", "研究中心", "research.html"],
  ["friend", "好友功能", "friend.html"],
  ["planet", "自律星球", "planet.html"],
  ["presentation", "專題發表流程", "presentation.html"],
];'''

content = re.sub(r'const modules = \[.*?\];', new_modules, content, flags=re.DOTALL)

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed app.js modules")
