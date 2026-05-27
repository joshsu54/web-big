import re

file_path = 'web_dashboard/planet.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to remove the label creation and appending logic
pattern_to_remove = r'''\s*const label = document\.createElement\('span'\);\s*label\.innerText = pName;\s*label\.style\.cssText = `[^`]+`;\s*planetDiv\.appendChild\(label\);'''

# Use regex to remove it
new_content = re.sub(pattern_to_remove, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Label removed from orbiting planets in planet.html!")
