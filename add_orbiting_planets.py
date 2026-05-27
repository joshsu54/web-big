import re

file_path = 'web_dashboard/planet.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add a specific orbit ring for the unlocked planets inside the view-solar-system
unlocked_orbit = '''
            <div class="orbit-line orbit-unlocked" id="unlockedPlanetsOrbit" style="width: 500px; height: 500px; animation-duration: 40s;">
              <!-- Unlocked planets will be injected here via JS -->
            </div>
'''
if 'id="unlockedPlanetsOrbit"' not in content:
    content = content.replace('<div class="orbit-line orbit-one">', unlocked_orbit + '\n            <div class="orbit-line orbit-one">')

# Add the JavaScript to fetch unlocked planets and render them
fetch_script = '''
    <script>
      // Fetch unlocked planets from backend and render them
      async function fetchUnlockedPlanets() {
        try {
          // In a real app, this ID comes from login session. We use an_nudge for demo.
          const res = await fetch('http://127.0.0.1:5001/api/user/an_nudge');
          const data = await res.json();
          if (data.success && data.user && data.user.planet && data.user.planet.unlocked) {
            const unlockedList = data.user.planet.unlocked;
            const orbitContainer = document.getElementById('unlockedPlanetsOrbit');
            if (orbitContainer) {
              orbitContainer.innerHTML = ''; // clear
              
              const colors = {
                  "新手星球": "#9ca3af",
                  "綠洲星球": "#34d399", 
                  "熔岩星球": "#ef4444", 
                  "冰雪星球": "#60a5fa", 
                  "沙漠星球": "#fbbf24", 
                  "水晶星球": "#a78bfa", 
                  "暗物質星球": "#8b5cf6"
              };
              
              // Only render if we have unlocked planets other than the base one
              const displayPlanets = unlockedList.filter(p => p !== "新手星球");
              
              if(displayPlanets.length > 0) {
                 displayPlanets.forEach((pName, index) => {
                    const angle = (360 / displayPlanets.length) * index;
                    const color = colors[pName] || "#ffffff";
                    
                    const planetDiv = document.createElement('div');
                    planetDiv.className = 'unlocked-planet-node';
                    planetDiv.style.cssText = `
                        position: absolute;
                        width: 24px;
                        height: 24px;
                        border-radius: 50%;
                        background: radial-gradient(circle at 30% 30%, #fff, ${color});
                        box-shadow: 0 0 20px ${color}, 0 0 40px ${color}88;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%) rotate(${angle}deg) translateX(250px) rotate(-${angle}deg);
                        animation: counter-rotate 40s linear infinite;
                    `;
                    
                    const label = document.createElement('span');
                    label.innerText = pName;
                    label.style.cssText = `
                        position: absolute;
                        top: 30px;
                        left: 50%;
                        transform: translateX(-50%);
                        color: #fff;
                        font-size: 10px;
                        white-space: nowrap;
                        text-shadow: 0 0 5px ${color};
                    `;
                    
                    planetDiv.appendChild(label);
                    orbitContainer.appendChild(planetDiv);
                 });
                 
                 // Add the CSS for counter-rotation if not present
                 if(!document.getElementById('unlockedPlanetStyles')) {
                     const style = document.createElement('style');
                     style.id = 'unlockedPlanetStyles';
                     style.innerHTML = `
                        @keyframes counter-rotate {
                            from { transform: translate(-50%, -50%) rotate(0deg) translateX(250px) rotate(0deg); }
                            to { transform: translate(-50%, -50%) rotate(360deg) translateX(250px) rotate(-360deg); }
                        }
                        .orbit-unlocked {
                            border: 1px dashed rgba(255,255,255,0.1);
                        }
                     `;
                     document.head.appendChild(style);
                 }
              }
            }
          }
        } catch (e) {
          console.warn("Backend not running or user not found, skipping planet fetch.", e);
        }
      }

      window.addEventListener('DOMContentLoaded', () => {
        // Fetch initially
        fetchUnlockedPlanets();
        // Poll every 5 seconds to see if a new planet was unlocked!
        setInterval(fetchUnlockedPlanets, 5000);
      });
    </script>
'''

content = content.replace('</body>', fetch_script + '\n  </body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated planet.html with dynamic orbiting unlocked planets!")
