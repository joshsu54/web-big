import re

file_path = 'web_dashboard/research.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the feature-grid
new_grid = '''<div class="feature-grid" style="grid-template-columns: 1fr 1fr; gap: 24px;">
            <article class="panel">
              <div class="panel-head">
                <strong>用戶睡眠時長分佈 (甜甜圈圖)</strong>
                <div class="panel-actions">
                  <span style="color:#f472b6; font-size:12px;">不足6h</span>
                  <span style="color:#a78bfa; font-size:12px; margin-left:8px;">6-8h</span>
                  <span style="color:#60a5fa; font-size:12px; margin-left:8px;">>8h</span>
                </div>
              </div>
              <div class="chart-container" style="height: 220px; position: relative;">
                <canvas id="researchSleepChart"></canvas>
              </div>
            </article>
            
            <article class="panel">
              <div class="panel-head">
                <strong>平均專注時間 (長條圖)</strong>
                <div class="panel-actions"><span style="color:#60a5fa; font-weight:bold;">本週趨勢</span></div>
              </div>
              <div class="chart-container" style="height: 220px;">
                <canvas id="researchFocusChart"></canvas>
              </div>
            </article>

            <article class="panel">
              <div class="panel-head">
                <strong>平均步數 (折線圖)</strong>
                <div class="panel-actions"><span style="color:#34d399; font-weight:bold;">今日 6,250 步</span></div>
              </div>
              <div class="chart-container" style="height: 220px;">
                <canvas id="researchStepsChart"></canvas>
              </div>
            </article>

            <article class="panel">
              <div class="panel-head">
                <strong>平均運動時間 (長條圖)</strong>
                <div class="panel-actions"><span style="color:#f472b6; font-weight:bold;">今日 25 分鐘</span></div>
              </div>
              <div class="chart-container" style="height: 220px;">
                <canvas id="researchExerciseChart"></canvas>
              </div>
            </article>
          </div>'''

content = re.sub(r'<div class="feature-grid".*?</article>\s*</div>', new_grid, content, flags=re.DOTALL)

# Replace the script block
new_script = '''<script src="assets/app.js?v=2"></script>
    <script>
      function drawBarChart(canvas, values, labels, color) {
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        const ratio = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * ratio;
        canvas.height = rect.height * ratio;
        ctx.scale(ratio, ratio);
        ctx.clearRect(0, 0, rect.width, rect.height);

        const pad = 30;
        const max = Math.max(...values) * 1.2;
        const step = (rect.width - pad * 2) / values.length;
        const barWidth = step * 0.5;
        
        values.forEach((value, i) => {
          const x = pad + i * step + (step - barWidth) / 2;
          const h = (value / max) * (rect.height - pad * 2);
          const y = rect.height - pad - h;
          
          ctx.fillStyle = color;
          ctx.shadowColor = color;
          ctx.shadowBlur = 15;
          ctx.beginPath();
          ctx.roundRect(x, y, barWidth, h, [6, 6, 0, 0]);
          ctx.fill();
          ctx.shadowBlur = 0;
          
          ctx.fillStyle = "#9ca3af";
          ctx.font = "12px system-ui";
          ctx.textAlign = "center";
          ctx.fillText(labels[i], x + barWidth/2, rect.height - 10);
        });
      }

      function drawCustomDonut(canvas, data, colors) {
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        const ratio = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * ratio;
        canvas.height = rect.height * ratio;
        ctx.scale(ratio, ratio);
        
        const cx = rect.width / 2;
        const cy = rect.height / 2;
        const r = Math.min(cx, cy) - 25;
        const total = data.reduce((a, b) => a + b, 0);
        
        let startAngle = -Math.PI / 2;
        data.forEach((val, i) => {
          const sliceAngle = (val / total) * 2 * Math.PI;
          ctx.beginPath();
          ctx.arc(cx, cy, r, startAngle, startAngle + sliceAngle);
          ctx.lineWidth = 18;
          ctx.strokeStyle = colors[i];
          ctx.shadowColor = colors[i];
          ctx.shadowBlur = 15;
          ctx.stroke();
          startAngle += sliceAngle;
        });

        ctx.shadowBlur = 0;
        ctx.fillStyle = "#fff";
        ctx.font = "bold 24px system-ui";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("6.8h", cx, cy - 5);
        ctx.fillStyle = "#9ca3af";
        ctx.font = "12px system-ui";
        ctx.fillText("平均", cx, cy + 15);
      }

      window.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
          // 1. Donut for Sleep
          drawCustomDonut(document.getElementById("researchSleepChart"), [20, 55, 25], ["#f472b6", "#a78bfa", "#60a5fa"]);
          
          // 2. Bar for Focus
          drawBarChart(document.getElementById("researchFocusChart"), [30, 45, 20, 60, 50, 80, 45], ["一", "二", "三", "四", "五", "六", "日"], "#60a5fa");
          
          // 3. Line for Steps (from app.js)
          if (typeof drawLineChart === 'function') {
            drawLineChart(document.getElementById("researchStepsChart"), [4000, 5200, 4800, 6000, 7500, 5500, 6250], "#34d399");
          }
          
          // 4. Bar for Exercise
          drawBarChart(document.getElementById("researchExerciseChart"), [10, 15, 0, 30, 45, 20, 25], ["一", "二", "三", "四", "五", "六", "日"], "#f472b6");
        }, 150);
      });
    </script>'''

content = re.sub(r'<script src="assets/app\.js\?v=2"></script>.*?</html>', new_script + '\n  </body>\n</html>', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated research.html with different charts!")
