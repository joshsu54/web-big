import re

file_path = 'web_dashboard/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Hero Section text
content = re.sub(
    r'<h1>.*?</h1>\s*<p>.*?</p>',
    r'<h1>Nudge Web 延伸平台：你的自律宇宙控制台。</h1>\n            <p>\n              這裡不只是手機 App 的數據大螢幕，更是你檢視「人生技能樹」、與好友互相拜訪星球、兌換商城專屬角色，以及掌握全站數據趨勢的專屬平台。\n            </p>',
    content,
    flags=re.DOTALL
)

# Replace tool-launch-grid
new_tool_grid = '''<section class="tool-launch-grid page-section">
          <a class="tool-launch-card" href="personal.html">
            <span>01</span>
            <strong>人生技能樹與天氣</strong>
            <p>將自律習慣轉化為技能升級與專屬的自律天氣預報。</p>
          </a>
          <a class="tool-launch-card" href="friend.html">
            <span>02</span>
            <strong>互動式好友清單</strong>
            <p>拜訪好友的專屬星球，並查看對方的專注與睡眠數據。</p>
          </a>
          <a class="tool-launch-card" href="operations.html">
            <span>03</span>
            <strong>自律商城兌換</strong>
            <p>使用任務獲得的自律幣，兌換常駐與限時專屬角色夥伴。</p>
          </a>
          <a class="tool-launch-card" href="research.html">
            <span>04</span>
            <strong>全站數據研究中心</strong>
            <p>透過多樣化圖表，分析全站用戶的平均睡眠、步數與專注趨勢。</p>
          </a>
        </section>'''
content = re.sub(r'<section class="tool-launch-grid page-section">.*?</section>', new_tool_grid, content, flags=re.DOTALL)

# Replace story-flow
new_story_flow = '''<section class="story-flow page-section">
          <article>
            <span>01</span>
            <h3>手機日常行動</h3>
            <p>任務、專注、健康追蹤先在 App 裡完成，累積自律點數與數據。</p>
          </article>
          <article>
            <span>02</span>
            <h3>網頁深度分析</h3>
            <p>Web 端將數據轉化為「自律天氣」、「壓力雷達」與「人生技能樹」。</p>
          </article>
          <article>
            <span>03</span>
            <h3>好友互相拜訪</h3>
            <p>透過 Web 端的互動好友列表，一鍵參觀好友努力養成的自律星球。</p>
          </article>
          <article>
            <span>04</span>
            <h3>成果可視化</h3>
            <p>純粹的 3D 星球與全站圖表，把抽象的努力變成可看見的世界與數據。</p>
          </article>
        </section>'''
content = re.sub(r'<section class="story-flow page-section">.*?</section>', new_story_flow, content, flags=re.DOTALL)

# Replace section-head for the features
content = re.sub(
    r'<span class="eyebrow">入口總覽</span>\s*<h2>六個 Web 延伸中心</h2>',
    r'<span class="eyebrow">入口總覽</span>\n            <h2>八大 Web 核心功能</h2>',
    content
)

# Replace feature-grid
new_feature_grid = '''<section class="feature-grid">
          <a class="feature-card" href="personal.html">
            <span class="icon">↗</span>
            <h3>個人進階分析中心</h3>
            <p>人生技能樹、自律天氣、壓力雷達、時間膠囊與未來的信。</p>
          </a>
          <a class="feature-card highlight" href="friend.html">
            <span class="icon">👥</span>
            <h3>好友功能</h3>
            <p>互動式好友清單，一鍵拜訪對方的自律星球、查看近期成就與詳細數值。</p>
          </a>
          <a class="feature-card" href="research.html">
            <span class="icon">⌁</span>
            <h3>研究中心</h3>
            <p>全站用戶的平均睡眠、專注、步數與運動數據的多樣化圖表分析。</p>
          </a>
          <a class="feature-card" href="operations.html">
            <span class="icon">◆</span>
            <h3>商城頁</h3>
            <p>使用自律幣兌換常駐、限時與活動專屬夥伴角色。</p>
          </a>
          <a class="feature-card highlight" href="planet.html">
            <span class="icon">✦</span>
            <h3>自律星球</h3>
            <p>純粹、無干擾的 3D 星球專屬展示空間，把分數變成可以被看見的宇宙。</p>
          </a>
          <a class="feature-card" href="guardian.html">
            <span class="icon">♡</span>
            <h3>家長陪伴中心</h3>
            <p>看趨勢、送鼓勵、設共同目標。重點是陪伴，不是監控。</p>
          </a>
          <a class="feature-card" href="groups.html">
            <span class="icon">◎</span>
            <h3>團體 / 教育管理中心</h3>
            <p>企業挑戰、補習班後台、讀書會挑戰、小組排行。</p>
          </a>
          <a class="feature-card" href="presentation.html">
            <span class="icon">▶</span>
            <h3>專題發表流程</h3>
            <p>把 App 核心、Web 延伸、自律星球與研究價值整理成可展示故事線。</p>
          </a>
        </section>'''
content = re.sub(r'<section class="feature-grid">.*?</section>', new_feature_grid, content, flags=re.DOTALL)

# Replace capability-matrix texts
new_matrix = '''<div class="matrix-grid">
            <div><small>個人</small><strong>深度洞察</strong><span>人生技能樹、自律天氣、壓力雷達</span></div>
            <div><small>社交</small><strong>好友拜訪</strong><span>互動列表、參觀星球、分享數據</span></div>
            <div><small>展示</small><strong>自律星球</strong><span>純粹 3D 展示、把努力轉成星球</span></div>
            <div><small>營運</small><strong>活動經濟</strong><span>常駐/限時商城、專屬角色兌換</span></div>
            <div><small>研究</small><strong>數據圖表</strong><span>全站平均睡眠、步數、專注圖表分析</span></div>
            <div><small>陪伴</small><strong>家長/教育</strong><span>共同目標、讀書會排行、鼓勵卡</span></div>
          </div>'''
content = re.sub(r'<div class="matrix-grid">.*?</div>', new_matrix, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html introductions!")
