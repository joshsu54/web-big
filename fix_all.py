import re
import os

# 1. Fix friend.html
friend_path = 'web_dashboard/friend.html'
with open(friend_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix sidebar
old_sidebar = '''<aside class="sidebar">
        <!-- Sidebar injected by app.js -->
      </aside>'''
new_sidebar = '''<aside class="sidebar">
        <a class="brand" href="index.html"><span class="brand-mark">N</span><span><strong>Nudge</strong><small>好友功能</small></span></a>
        <nav class="nav">
          <!-- Sidebar injected by app.js -->
        </nav>
      </aside>'''
if old_sidebar in content:
    content = content.replace(old_sidebar, new_sidebar)
else:
    print("Warning: old_sidebar not found in friend.html")

# Fix Tabs and Add Mock Avatar/Planet sync
tab_script = '''
      // 切換好友清單的子頁籤
      function switchFriendTab(tabName, btnElement) {
        document.querySelectorAll('.friend-tab').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
        
        const listContainer = document.querySelector('.friend-list');
        if(tabName === '申請') {
          listContainer.innerHTML = '<div style="text-align:center; padding: 40px; color:#9ca3af;">目前有 3 個好友申請，等待確認中...</div>';
        } else if(tabName === '搜尋') {
          listContainer.innerHTML = '<div style="text-align:center; padding: 40px;"><input type="text" placeholder="輸入好友 ID..." style="padding:10px; border-radius:8px; border:1px solid #444; background:#2a2a40; color:#fff;"/><button class="button primary" style="margin-left:10px;">搜尋</button></div>';
        } else {
          // 重新載入列表 (為了示範，重新整理頁面)
          window.location.reload();
        }
      }

      // 模擬連線手機端：抓取真實的好友頭像與星球
      async function syncMobileFriendData(friendId) {
        console.log(`正在與手機端同步好友 ${friendId} 的真實星球與頭像資料...`);
        // 這裡可以透過 Firebase 或是 Flutter Web 通訊橋樑抓取真實 SVG / 模型
        // return await firebase.firestore().collection('users').doc(friendId).get();
      }
'''
if 'function showFriendDetail(' in content and 'switchFriendTab' not in content:
    content = content.replace('function showFriendDetail(', tab_script + '\n      function showFriendDetail(')

# Update HTML for tabs to call switchFriendTab
content = content.replace('<button class="friend-tab active">好友列表</button>', '<button class="friend-tab active" onclick="switchFriendTab(\'列表\', this)">好友列表</button>')
content = content.replace('<button class="friend-tab">好友申請 <span', '<button class="friend-tab" onclick="switchFriendTab(\'申請\', this)">好友申請 <span')
content = content.replace('<button class="friend-tab">好友搜尋</button>', '<button class="friend-tab" onclick="switchFriendTab(\'搜尋\', this)">好友搜尋</button>')

# Update showFriendDetail to call the mock function
mock_call = '''// 連線並偵測好友自身的真實星球樣子與頭像
        syncMobileFriendData(id);'''
if mock_call not in content:
    content = content.replace('// Update DOM elements', mock_call + '\\n        // Update DOM elements')

with open(friend_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated friend.html")

# 2. Fix operations.html (Mock shop items if fetch fails)
ops_path = 'web_dashboard/operations.html'
with open(ops_path, 'r', encoding='utf-8') as f:
    ops_content = f.read()

mock_items = '''
        // 備用示範資料 (若後台 fetch 失敗時呈現)
        const mockShopItems = [
          { name: "專注精靈 (藍)", type: "permanent", price: 1500, image_path: "assets/character1.png" },
          { name: "自律法師", type: "permanent", price: 2500, image_path: "assets/character2.png" },
          { name: "時間刺客", type: "limited", price: 3000, image_path: "assets/character3.png", end_time: Date.now()/1000 + 86400*3 },
          { name: "聖誕雪人", type: "event_character", price: 800, image_path: "assets/character4.png", end_time: Date.now()/1000 + 86400*7 }
        ];
'''

if 'const mockShopItems =' not in ops_content:
    ops_content = ops_content.replace('let allActiveItems = [];', mock_items + '\n      let allActiveItems = [];')
    
    fetch_logic = '''if (result.success && result.items && result.items.length > 0) {
            allActiveItems = result.items;
          } else {
            allActiveItems = mockShopItems;
          }'''
    ops_content = ops_content.replace('allActiveItems = result.items;', fetch_logic)
    
    catch_logic = '''console.error("無法取得上架商品", error);
          allActiveItems = mockShopItems;'''
    ops_content = ops_content.replace('console.error("無法取得上架商品", error);', catch_logic)
    
    with open(ops_path, 'w', encoding='utf-8') as f:
        f.write(ops_content)
    print("Updated operations.html")

# 3. Fix research.html
res_path = 'web_dashboard/research.html'
with open(res_path, 'r', encoding='utf-8') as f:
    res_content = f.read()

# Remove subnav completely from research.html
res_content = re.sub(r'<div class="subnav".*?</div>', '', res_content, flags=re.DOTALL)
# Also fix the subnav if it was in the hero or page-section
res_content = re.sub(r'<div class="page-section" style="padding-bottom: 0; padding-top: 20px;">\s*</div>', '', res_content, flags=re.DOTALL)

with open(res_path, 'w', encoding='utf-8') as f:
    f.write(res_content)
print("Updated research.html")

# Delete the other research files
for file in ['research-scenario.html', 'research-anonymized.html', 'research-score-demo.html']:
    full_path = os.path.join('web_dashboard', file)
    if os.path.exists(full_path):
        os.remove(full_path)
        print(f"Deleted {file}")
