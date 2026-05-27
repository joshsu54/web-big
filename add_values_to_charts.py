import re

file_path = 'web_dashboard/research.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the script block with one that includes value rendering for Bar, Donut, and a custom Line chart function.
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
        const max = Math.max(...values) * 1.3; // increase max slightly to leave room for text
        const step = (rect.width - pad * 2) / values.length;
        const barWidth = step * 0.5;
        
        values.forEach((value, i) => {
          const x = pad + i * step + (step - barWidth) / 2;
          const h = (value / max) * (rect.height - pad * 2);
          const y = rect.height - pad - h;
          
          // Draw Bar
          ctx.fillStyle = color;
          ctx.shadowColor = color;
          ctx.shadowBlur = 15;
          ctx.beginPath();
          ctx.roundRect(x, y, barWidth, h, [6, 6, 0, 0]);
          ctx.fill();
          ctx.shadowBlur = 0;
          
          // Draw Label (X-axis)
          ctx.fillStyle = "#9ca3af";
          ctx.font = "12px system-ui";
          ctx.textAlign = "center";
          ctx.fillText(labels[i], x + barWidth/2, rect.height - 10);
          
          // Draw Value (Top of bar)
          ctx.fillStyle = "#fff";
          ctx.font = "bold 12px system-ui";
          ctx.fillText(value, x + barWidth/2, y - 8);
        });
      }

      function drawCustomDonut(canvas, data, colors, labels) {
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
          
          // Draw Slice
          ctx.beginPath();
          ctx.arc(cx, cy, r, startAngle, startAngle + sliceAngle);
          ctx.lineWidth = 18;
          ctx.strokeStyle = colors[i];
          ctx.shadowColor = colors[i];
          ctx.shadowBlur = 15;
          ctx.stroke();
          
          // Draw Value text near the slice
          const textAngle = startAngle + sliceAngle / 2;
          const textR = r + 20; // push text outside the donut
          const tx = cx + textR * Math.cos(textAngle);
          const ty = cy + textR * Math.sin(textAngle);
          
          ctx.shadowBlur = 0;
          ctx.fillStyle = "#fff";
          ctx.font = "bold 12px system-ui";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(val + "%", tx, ty);
          
          startAngle += sliceAngle;
        });

        // Center Text
        ctx.fillStyle = "#fff";
        ctx.font = "bold 24px system-ui";
        ctx.fillText("6.8h", cx, cy - 5);
        ctx.fillStyle = "#9ca3af";
        ctx.font = "12px system-ui";
        ctx.fillText("平均", cx, cy + 15);
      }
      
      // Custom Line Chart for Research with Values displayed
      function drawValueLineChart(canvas, values, labels, color) {
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
        const min = Math.min(...values) * 0.8;
        const range = max - min;
        const step = (rect.width - pad * 2) / (values.length - 1);
        
        // Draw Line
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.shadowColor = color;
        ctx.shadowBlur = 15;
        
        const points = [];
        values.forEach((value, i) => {
          const x = pad + i * step;
          const y = rect.height - pad - ((value - min) / range) * (rect.height - pad * 2);
          points.push({x, y, value, label: labels[i]});
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.shadowBlur = 0;
        
        // Draw points, values, and labels
        points.forEach(p => {
          // Circle point
          ctx.beginPath();
          ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
          ctx.fillStyle = "#fff";
          ctx.fill();
          ctx.strokeStyle = color;
          ctx.lineWidth = 2;
          ctx.stroke();
          
          // X-axis label
          ctx.fillStyle = "#9ca3af";
          ctx.font = "12px system-ui";
          ctx.textAlign = "center";
          ctx.fillText(p.label, p.x, rect.height - 10);
          
          // Value text above point
          ctx.fillStyle = "#fff";
          ctx.font = "bold 11px system-ui";
          ctx.fillText(p.value, p.x, p.y - 12);
        });
      }

      window.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
          // 1. Donut for Sleep (Added percentages next to slices)
          drawCustomDonut(document.getElementById("researchSleepChart"), [20, 55, 25], ["#f472b6", "#a78bfa", "#60a5fa"], ["不足6h", "6-8h", "超過8h"]);
          
          // 2. Bar for Focus (Values displayed on top of bars)
          drawBarChart(document.getElementById("researchFocusChart"), [30, 45, 20, 60, 50, 80, 45], ["一", "二", "三", "四", "五", "六", "日"], "#60a5fa");
          
          // 3. Line for Steps (Customized to show points and values)
          drawValueLineChart(document.getElementById("researchStepsChart"), [4000, 5200, 4800, 6000, 7500, 5500, 6250], ["一", "二", "三", "四", "五", "六", "日"], "#34d399");
          
          // 4. Bar for Exercise (Values displayed on top of bars)
          drawBarChart(document.getElementById("researchExerciseChart"), [10, 15, 0, 30, 45, 20, 25], ["一", "二", "三", "四", "五", "六", "日"], "#f472b6");
        }, 150);
      });
    </script>'''

content = re.sub(r'<script src="assets/app\.js\?v=2"></script>.*?</html>', new_script + '\n  </body>\n</html>', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated research.html charts to include values!")
