import os
import re
import glob

def clean_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove link to personal-template.html
    content = re.sub(r'<a[^>]*href="personal-template\.html"[^>]*>.*?</a>', '', content)
    
    # 2. Remove references to "任務模板" in text
    content = content.replace('讀書會任務模板、', '讀書會挑戰、')
    content = content.replace('任務模板、', '')
    content = content.replace('任務模板', '挑戰功能')

    # 3. Clean up any remaining references to planet-builder.html
    content = re.sub(r'<a[^>]*href="planet-builder\.html"[^>]*>.*?</a>', '', content)

    # 4. Remove card sections for task template in personal.html
    # In personal.html there's a card for "任務模板產生器"
    # "<strong>任務模板產生器</strong>...<small>產生任務模板</small>"
    content = re.sub(r'<a class="hub-card"[^>]*href="personal-template\.html".*?</a>', '', content, flags=re.DOTALL)
    
    # Also clean up any loose references to "星球規劃"
    content = content.replace('星球規劃器', '')
    content = content.replace('星球規劃', '')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('web_dashboard/*.html'):
    clean_file(f)
print("Cleaned up remaining artifacts")
