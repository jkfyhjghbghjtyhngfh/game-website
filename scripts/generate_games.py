#!/usr/bin/env python3
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAMES_DIR = ROOT / 'games'

N = int(sys.argv[1]) if len(sys.argv) > 1 else 250

GAMES_DIR.mkdir(exist_ok=True)

print(f'Generating {N} placeholder games in {GAMES_DIR}...')

for i in range(1, N+1):
    key = f'game-{i:03d}'
    d = GAMES_DIR / key
    d.mkdir(exist_ok=True)
    index = d / 'index.html'
    if index.exists():
        continue
    title = f'Placeholder Game {i:03d}'
    index.write_text(f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{title}</title>
<style>body{{font-family:system-ui,Arial,sans-serif;padding:2rem}}.btn{{display:inline-block;padding:0.5rem 0.75rem;background:#0366d6;color:#fff;border-radius:4px;text-decoration:none}}</style>
</head>
<body>
  <h1>{title}</h1>
  <p>This is a placeholder page for {title}. Replace with the real game files (HTML/JS/assets) to host the game here.</p>
  <p><a class='btn' href='../games.html'>Back to Games</a> <a class='btn' href='#' onclick="alert('No game bundled yet');return false;">Play (placeholder)</a></p>
</body>
</html>""")

# Build a games index page
print('Building games.html...')
entries = []
for i in range(1, N+1):
    key = f'game-{i:03d}'
    title = f'Placeholder Game {i:03d}'
    # simple SVG thumbnail data URI
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='300' height='180'>"
           f"<rect width='100%' height='100%' fill='#111'/>"
           f"<text x='50%' y='50%' fill='#ddd' font-family='sans-serif' font-size='18' dominant-baseline='middle' text-anchor='middle'>{title}</text>"
           "</svg>")
    datauri = 'data:image/svg+xml;utf8,' + svg.replace('\n','')
    entries.append((key, title, datauri))

games_html = """<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>All Games</title>
<style>
  body{font-family:system-ui,Arial;margin:1rem}
  .games{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
  .card{border:1px solid #ddd;padding:8px;border-radius:6px;background:#fff}
  .thumb{width:100%;height:120px;object-fit:cover;background:#111}
  .meta{margin-top:6px}
  .btn{display:inline-block;padding:0.35rem 0.5rem;background:#0366d6;color:#fff;border-radius:4px;text-decoration:none}
  .pager{margin-top:12px}
</style>
</head>
<body>
  <h1>Games</h1>
  <p>Generated placeholder games. Replace with actual game pages and assets when available.</p>
  <div id="games" class="games"></div>
  <div class="pager">
    <button id="prev">Prev</button>
    <span id="pageInfo"></span>
    <button id="next">Next</button>
  </div>

<script>
  const entries = [
"""

for key, title, datauri in entries:
    games_html += f"    {{id: '{key}', title: '{title}', thumb: '{datauri}'}},\n"

games_html += """];
  const perPage = 24;
  let page = 0;
  function render(){
    const start = page*perPage;
    const slice = entries.slice(start, start+perPage);
    const container = document.getElementById('games');
    container.innerHTML = '';
    slice.forEach(e => {
      const div = document.createElement('div');
      div.className = 'card';
      div.innerHTML = `<img class='thumb' src='${e.thumb}' alt=''/>` +
                      `<div class='meta'><strong>${e.title}</strong><br><a class='btn' href='games/${e.id}/index.html'>Open</a></div>`;
      container.appendChild(div);
    });
    document.getElementById('pageInfo').textContent = `Page ${page+1} of ${Math.ceil(entries.length/perPage)}`;
  }
  document.getElementById('prev').addEventListener('click', ()=>{if(page>0){page--;render();}});
  document.getElementById('next').addEventListener('click', ()=>{if((page+1)*perPage<entries.length){page++;render();}});
  render();
</script>
</body>
</html>"""

with open(ROOT / 'games.html', 'w') as f:
    f.write(games_html)

print('Done.')
