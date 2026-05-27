import os
import re

file_path = 'web_dashboard/server.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new backend APIs and game logic
api_code = '''
# ==========================================
# User Data & Mobile Sync APIs
# ==========================================
import random

USER_DATA_FILE = os.path.join(UPLOAD_FOLDER, 'users_data.json')

def load_all_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_all_users(data):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user(user_id):
    users = load_all_users()
    if user_id not in users:
        users[user_id] = {
            "user_id": user_id,
            "name": user_id,
            "avatar": "🧑‍🚀",
            "planet": {
                "name": "新手星球",
                "level": 1,
                "color": "#9ca3af",
                "unlocked": ["新手星球"]
            },
            "stats": {
                "focus_minutes": 0,
                "steps": 0,
                "sleep_hours": 0.0,
                "exercise_minutes": 0
            },
            "status": "努力自律中",
            "current_goal": "無"
        }
    return users[user_id]

def update_user(user_id, updates):
    users = load_all_users()
    user = get_user(user_id)
    
    # Recursively update dictionary
    def recursive_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = recursive_update(d.get(k, {}), v)
            else:
                d[k] = v
        return d
        
    updated_user = recursive_update(user, updates)
    users[user_id] = updated_user
    save_all_users(users)
    return updated_user

@app.route('/api/sync/user', methods=['POST'])
def sync_user():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    
    # Example payload: {"user_id": "an_nudge", "name": "小安", "avatar": "🧑‍🚀", "status": "被專題快搞瘋了"}
    user_id = data.pop('user_id')
    user = update_user(user_id, data)
    return jsonify({"success": True, "user": user})

@app.route('/api/sync/health', methods=['POST'])
def sync_health():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    
    user_id = data.pop('user_id')
    
    # Map health data to stats
    stats_update = {"stats": {}}
    if 'sleep_hours' in data: stats_update["stats"]["sleep_hours"] = data['sleep_hours']
    if 'steps' in data: stats_update["stats"]["steps"] = data['steps']
    if 'exercise_minutes' in data: stats_update["stats"]["exercise_minutes"] = data['exercise_minutes']
    
    user = update_user(user_id, stats_update)
    return jsonify({"success": True, "message": "Health synced", "user": user})

@app.route('/api/sync/focus', methods=['POST'])
def sync_focus():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    
    user_id = data.pop('user_id')
    user = get_user(user_id)
    
    # Gamification Logic: Weekly Task Completion -> Planet Unlock
    newly_unlocked = None
    tasks_completed = data.get('tasks_completed', 0)
    tasks_total = data.get('tasks_total', 1)
    
    if tasks_total > 0:
        completion_rate = tasks_completed / tasks_total
        if completion_rate >= 0.7:
            planets_pool = ["綠洲星球", "熔岩星球", "冰雪星球", "沙漠星球", "水晶星球", "暗物質星球"]
            current_unlocked = set(user.get("planet", {}).get("unlocked", []))
            
            # Find planets not yet unlocked
            available_planets = [p for p in planets_pool if p not in current_unlocked]
            
            if available_planets:
                # Randomly unlock a new one
                newly_unlocked = random.choice(available_planets)
                user["planet"].setdefault("unlocked", []).append(newly_unlocked)
                # Automatically equip the new planet (optional, but gives a cool effect)
                user["planet"]["name"] = newly_unlocked
                
                # Level up the base planet system
                user["planet"]["level"] = user["planet"].get("level", 1) + 1
                
                # Assign a color based on planet type
                colors = {
                    "綠洲星球": "#34d399", "熔岩星球": "#ef4444", 
                    "冰雪星球": "#60a5fa", "沙漠星球": "#fbbf24", 
                    "水晶星球": "#a78bfa", "暗物質星球": "#8b5cf6"
                }
                user["planet"]["color"] = colors.get(newly_unlocked, "#ffffff")

    # Update focus stats
    if 'focus_minutes' in data:
        user.setdefault("stats", {})["focus_minutes"] = data['focus_minutes']
    if 'current_goal' in data:
        user["current_goal"] = data['current_goal']
        
    users = load_all_users()
    users[user_id] = user
    save_all_users(users)
    
    return jsonify({
        "success": True, 
        "message": "Focus synced",
        "new_planet_unlocked": newly_unlocked,
        "user": user
    })

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_api(user_id):
    user = get_user(user_id)
    return jsonify({"success": True, "user": user})
    
'''

if 'def sync_user():' not in content:
    # Insert before the __main__ block
    content = content.replace("if __name__ == '__main__':", api_code + "\nif __name__ == '__main__':")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Backend API implemented!")
else:
    print("Backend API already exists!")
