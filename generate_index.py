#!/usr/bin/env python3
"""
Generate a simple index.html page listing all downloaded GeoJSON files
No styling. Just links. 1994 style.
"""

import os
from datetime import datetime

def generate_index_html():
    """Generate simple index.html with links to all GeoJSON files"""
    
    # Configuration
    base_github_url = "https://dvanauken.github.io/data"
    features_root = "features"
    
    # Check if features directory exists
    if not os.path.exists(features_root):
        print(f"ERROR: Directory '{features_root}' not found!")
        return
    
    # Scan directory structure and collect GeoJSON files
    geojson_files = []
    
    for root, dirs, files in os.walk(features_root):
        for file in files:
            if file.endswith('.geojson'):
                rel_path = os.path.relpath(os.path.join(root, file))
                url_path = rel_path.replace('\\', '/')
                full_url = f"{base_github_url}/{url_path}"
                
                geojson_files.append({
                    'filename': file,
                    'url': full_url
                })
    
    # Sort files alphabetically
    geojson_files.sort(key=lambda x: x['filename'])
    
    # Generate simple HTML
    html = f"""<html>
<head>
<title>Natural Earth GeoJSON Files</title>
</head>
<body>
<h1>Natural Earth GeoJSON Files</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<p>Total files: {len(geojson_files)}</p>
<hr>
<ul>
"""
    
    for file_info in geojson_files:
        html += f'<li><a href="{file_info["url"]}">{file_info["filename"]}</a></li>\n'
    
    html += """</ul>
</body>
</html>"""
    
    # Write index.html
    with open('index.html', 'w') as f:
        f.write(html)
    
    print(f"Generated index.html with {len(geojson_files)} files")

if __name__ == "__main__":
    generate_index_html()