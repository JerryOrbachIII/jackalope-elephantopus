#!/usr/bin/env python3
"""
YouTube 0-View Video Finder - OPENS IN YOUTUBE APP
Automatically opens videos in the YouTube app on iOS
"""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import urllib.request
import random
import ssl
from datetime import datetime, timedelta
import socket

# Recommendation: Use environment variables for secrets
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyB6aUWCKx4tM9zN4fBzhZdRSj8Zlpcw7NA")

# Mapping of device prefixes to their common date formats
DEVICE_PREFIXES = {
    'WIN': {'name': 'Webcam', 'formats': 'YMD'},
    'VID': {'name': 'Generic Camera', 'formats': 'YMD,MDY,DMY'},
    'MVI': {'name': 'Canon', 'formats': 'YMD,DMY'},
    'GOPR': {'name': 'GoPro', 'formats': 'MDY'},
    'DJI': {'name': 'DJI Drone', 'formats': 'YMD'},
    'DSC': {'name': 'Sony', 'formats': 'YMD,DMY'},
    'DSCN': {'name': 'Nikon', 'formats': 'YMD,DMY'},
    'PXL': {'name': 'Google Pixel', 'formats': 'MDY'},
    'IMG': {'name': 'Camera', 'formats': 'YMD,DMY'},
    'MOV': {'name': 'Apple/Camera', 'formats': 'MDY,DMY'},
    'RPReplay': {'name': 'iOS Screen Recording', 'formats': 'MDY'},
}

HTML_PAGE = '''<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">
    <title>0-View Video Finder</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        h1 {
            color: #FF0000;
            text-align: center;
            margin-bottom: 10px;
            font-size: 24px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }
        button {
            width: 100%;
            background: #FF0000;
            color: white;
            border: none;
            padding: 20px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            margin: 20px 0;
            cursor: pointer;
            -webkit-tap-highlight-color: transparent;
            transition: transform 0.1s;
        }
        button:active { background: #CC0000; transform: scale(0.98); }
        button:disabled { background: #ccc; }
        .option {
            margin: 15px 0;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            background: white;
        }
        #status {
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
            min-height: 20px;
            display: none;
        }
        .success { background: #d4edda; color: #155724; display: block; }
        .error { background: #f8d7da; color: #721c24; display: block; }
        .searching { background: #fff3cd; color: #856404; display: block; }
        .zero-badge {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: bold;
        }
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 12px;
            margin: 15px 0;
            font-size: 13px;
            border-radius: 4px;
        }
        a.manual-link {
            display: inline-block;
            margin-top: 8px;
            color: #007bff;
            text-decoration: none;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎥 0-View Video Finder</h1>
        <div class="subtitle">Opens videos in YouTube app</div>

        <div class="info-box">
            📱 Videos will open in the YouTube app automatically
        </div>

        <div class="option">
            <label>Device Type:</label>
            <select id="prefix">
                <option value="random">🎲 Random</option>
                <option value="WIN">WIN (Webcam)</option>
                <option value="VID">VID (Camera)</option>
                <option value="MVI">MVI (Canon)</option>
                <option value="GOPR">GOPR (GoPro)</option>
                <option value="DJI">DJI (Drone)</option>
                <option value="DSC">DSC (Sony)</option>
                <option value="DSCN">DSCN (Nikon)</option>
                <option value="PXL">PXL (Pixel)</option>
                <option value="IMG">IMG (Camera)</option>
                <option value="MOV">MOV (Apple)</option>
                <option value="RPReplay">RPReplay (iOS)</option>
            </select>
        </div>

        <div class="option">
            <label>Date Range:</label>
            <select id="dateRange">
                <option value="7">Last week</option>
                <option value="30" selected>Last month</option>
                <option value="90">Last 3 months</option>
                <option value="180">Last 6 months</option>
            </select>
        </div>

        <div class="option">
            <label>Max Views:</label>
            <select id="maxViews">
                <option value="0" selected>0 views only</option>
                <option value="5">Under 5 views</option>
                <option value="10">Under 10 views</option>
                <option value="50">Under 50 views</option>
                <option value="100">Under 100 views</option>
            </select>
        </div>

        <button onclick="findVideo()">🎲 Find & Open Video</button>

        <div id="status"></div>
    </div>

    <script>
        let controller = null;

        async function findVideo() {
            if (controller) controller.abort();
            controller = new AbortController();

            const btn = document.querySelector('button');
            const status = document.getElementById('status');
            const prefix = document.getElementById('prefix').value;
            const days = document.getElementById('dateRange').value;
            const maxViews = document.getElementById('maxViews').value;

            btn.disabled = true;
            btn.textContent = '🔍 Searching...';
            status.className = 'searching';
            status.textContent = 'Searching for videos with ≤' + maxViews + ' views...';

            try {
                const url = '/api/find?prefix=' + encodeURIComponent(prefix) +
                           '&days=' + encodeURIComponent(days) +
                           '&max_views=' + encodeURIComponent(maxViews);

                const response = await fetch(url, { signal: controller.signal });
                const data = await response.json();

                if (data.error) {
                    status.className = 'error';
                    status.innerHTML = '❌ ' + data.error;
                    btn.disabled = false;
                    btn.textContent = '🎲 Find & Open Video';
                } else {
                    const badge = '<span class="zero-badge">' + data.views + ' VIEWS</span>';

                    const videoId = data.id;
                    const youtubeAppUrl = 'youtube://watch?v=' + videoId;
                    const webUrl = data.url;

                    status.className = 'success';
                    status.innerHTML =
                        '✅ Found! ' + badge + '<br>' +
                        '<small style="color:#666;">Query: ' + data.query + '</small><br>' +
                        '<small style="color:#666;">Checked ' + data.checked + ' videos</small><br>' +
                        '<small style="color:#666;">Opening YouTube app...</small>' +
                        '<a href="' + webUrl + '" class="manual-link" target="_blank">Open in browser instead</a>';

                    // Try to open in YouTube app
                    setTimeout(() => {
                        window.location.href = youtubeAppUrl;
                    }, 1000);

                    // Re-enable button after delay
                    setTimeout(() => {
                        btn.disabled = false;
                        btn.textContent = '🎲 Find & Open Video';
                    }, 3000);
                }
            } catch (e) {
                if (e.name === 'AbortError') {
                    status.className = 'error';
                    status.textContent = '❌ Canceled';
                } else {
                    status.className = 'error';
                    status.textContent = '❌ Error: ' + e.message;
                }
                btn.disabled = false;
                btn.textContent = '🎲 Find & Open Video';
            } finally {
                controller = null;
            }
        }
    </script>
</body>
</html>'''

def generate_date_variations(date_obj, formats):
    variations = []
    y, ys, m, d = date_obj.strftime('%Y'), date_obj.strftime('%y'), date_obj.strftime('%m'), date_obj.strftime('%d')

    for fmt in formats.split(','):
        fmt = fmt.strip()
        if fmt == 'YMD':
            variations.extend([f"{y}{m}{d}", f"{ys}{m}{d}"])
        elif fmt == 'DMY':
            variations.extend([f"{d}{m}{y}", f"{d}{m}{ys}"])
        elif fmt == 'MDY':
            variations.extend([f"{m}{d}{y}", f"{m}{d}{ys}"])
    return variations

def search_youtube_api(query, max_results=50):
    """Search YouTube and get video IDs with view counts."""
    try:
        # Search for videos
        search_params = {
            'part': 'id',
            'q': query,
            'type': 'video',
            'maxResults': min(max_results, 50),
            'order': 'date',
            'key': YOUTUBE_API_KEY
        }

        search_url = f'https://www.googleapis.com/youtube/v3/search?{urllib.parse.urlencode(search_params)}'
        req = urllib.request.Request(search_url)

        with urllib.request.urlopen(req, timeout=15) as resp:
            search_data = json.loads(resp.read().decode('utf-8'))

        if 'items' not in search_data or not search_data['items']:
            return []

        # Extract video IDs
        video_ids = [item['id'].get('videoId') for item in search_data['items'] if 'videoId' in item['id']]

        if not video_ids:
            return []

        # Get video statistics
        video_params = {
            'part': 'statistics',
            'id': ','.join(video_ids),
            'key': YOUTUBE_API_KEY
        }

        video_url = f'https://www.googleapis.com/youtube/v3/videos?{urllib.parse.urlencode(video_params)}'
        req = urllib.request.Request(video_url)

        with urllib.request.urlopen(req, timeout=15) as resp:
            video_data = json.loads(resp.read().decode('utf-8'))

        # Build results with view counts
        results = []
        for item in video_data.get('items', []):
            vid_id = item['id']
            views = int(item['statistics'].get('viewCount', 0))
            results.append({'id': vid_id, 'views': views})

        return results

    except Exception as e:
        print(f"API Error: {e}")
        return None

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_safe_response(self, code, content_type, data):
        try:
            self.send_response(code)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', len(data))
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError, socket.error):
            pass

    def do_GET(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            if parsed_path.path == '/':
                self.send_safe_response(200, 'text/html; charset=utf-8', HTML_PAGE.encode('utf-8'))

            elif parsed_path.path == '/api/find':
                params = urllib.parse.parse_qs(parsed_path.query)
                try:
                    prefix = params.get('prefix', ['random'])[0]
                    days = int(params.get('days', ['30'])[0])
                    max_views = int(params.get('max_views', ['0'])[0])
                except (ValueError, IndexError) as e:
                    error = {'error': f'Invalid parameters: {str(e)}'}
                    self.send_safe_response(400, 'application/json', json.dumps(error).encode('utf-8'))
                    return

                try:
                    # Try multiple searches
                    max_attempts = 15
                    checked_count = 0

                    for attempt in range(max_attempts):
                        # Pick prefix
                        current_prefix = prefix
                        if prefix == 'random' or prefix not in DEVICE_PREFIXES:
                            current_prefix = random.choice(list(DEVICE_PREFIXES.keys()))

                        # Generate random date
                        date = datetime.now() - timedelta(days=random.randint(0, days))
                        formats = DEVICE_PREFIXES[current_prefix]['formats']

                        # Generate query
                        date_str = random.choice(generate_date_variations(date, formats))
                        query = random.choice([
                            f"{current_prefix} {date_str}",
                            f"{current_prefix}({date_str})",
                            f"{current_prefix}_{date_str}"
                        ])

                        print(f"[{attempt+1}/{max_attempts}] {query}")

                        # Search with API
                        results = search_youtube_api(query, max_results=50)

                        if results is None:
                            error = {'error': 'API request failed. Check your API key or quota.'}
                            self.send_safe_response(500, 'application/json', json.dumps(error).encode('utf-8'))
                            return

                        checked_count += len(results)

                        # Filter by view count
                        matching = [v for v in results if v['views'] <= max_views]

                        if matching:
                            video = random.choice(matching)
                            result = {
                                'id': video['id'],
                                'url': f'https://www.youtube.com/watch?v={video["id"]}',
                                'query': query,
                                'views': video['views'],
                                'checked': checked_count
                            }
                            print(f"✓ Found {video['views']}-view video! ID: {video['id']}")
                            self.send_safe_response(200, 'application/json', json.dumps(result).encode('utf-8'))
                            return

                    # No matching videos found
                    error = {'error': f'No videos with ≤{max_views} views found after checking {checked_count} videos. Try again!'}
                    print(f"✗ No matches after checking {checked_count} videos")
                    self.send_safe_response(404, 'application/json', json.dumps(error).encode('utf-8'))

                except Exception as e:
                    print(f"Error: {e}")
                    error = {'error': f'Search error: {str(e)}'}
                    self.send_safe_response(500, 'application/json', json.dumps(error).encode('utf-8'))

            else:
                self.send_safe_response(404, 'text/plain', b'Not Found')

        except (BrokenPipeError, ConnectionResetError, socket.error):
            pass
        except Exception as e:
            print(f"Handler error: {e}")

if __name__ == '__main__':
    PORT = 8080

    print('\n' + '='*60)
    print('🎥 YouTube 0-View Video Finder - YouTube App Version')
    print('='*60)
    print(f'✓ API Key: {"from environment" if "YOUTUBE_API_KEY" in os.environ else "using default"}')
    print('✓ Opens videos in YouTube app automatically')
    print('='*60 + '\n')

    HTTPServer.allow_reuse_address = True

    try:
        server = HTTPServer(('', PORT), Handler)
        server.timeout = 60

        print(f'🚀 Server running!')
        print(f'📱 Open Safari to: http://localhost:{PORT}\n')
        print('How it works:')
        print('  1. Click "Find & Open Video"')
        print('  2. Wait while it searches')
        print('  3. YouTube app opens automatically with the video\n')
        print('Note: Keep this page open to find more videos!\n')
        print('Press Ctrl+C to stop\n')

        server.serve_forever()

    except KeyboardInterrupt:
        print('\n\n👋 Server stopped')
    except OSError as e:
        if e.errno == 48:
            print(f'\n❌ Port {PORT} already in use!')
        else:
            print(f'\n❌ Error: {e}')
