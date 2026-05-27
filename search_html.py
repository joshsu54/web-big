import os, re

def search(keywords):
    patterns = {kw: re.compile(kw) for kw in keywords}
    for r, d, files in os.walk('web_dashboard'):
        for f in files:
            if not f.endswith('.html'): continue
            path = os.path.join(r, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    for i, line in enumerate(file):
                        for kw, p in patterns.items():
                            if p.search(line):
                                print(f"{kw} found in {path}:{i+1}: {line.strip()}")
            except Exception as e:
                pass

search(["任務模板", "研究展示中心", "自律星球規劃", "事件", "好友", "研究", "星球", "模板"])
