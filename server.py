from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Alapértelmezett hangerők (0-100 skálán)
DEFAULT_YOUTUBE_VOLUME = 30  # 30%
DEFAULT_FACEBOOK_VOLUME = 100  # 100%

def convert_to_scalar(volume_percent):
    """0-100 közötti szám átalakítása 0-1 közé (scalar value)"""
    volume_percent = max(0, min(100, volume_percent))  # 0-100 közé korlátozás
    return volume_percent / 100.0

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'Szerver fut!')
    
    def do_POST(self):
        print("🔵 POST kérés érkezett!")
        
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                url = data.get('url', '')
                print(f"🔵 URL: {url}")
                
                if 'youtube.com' in url:
                    print("🔵 YouTube észlelve")
                    script_path = os.path.join(SCRIPT_DIR, "youtube_volume.py")
                    volume_percent = get_youtube_volume()
                    volume_scalar = convert_to_scalar(volume_percent)
                    subprocess.Popen(["python", script_path, str(volume_scalar)])
                    
                elif 'facebook.com' in url:
                    print("🔵 Facebook észlelve")
                    script_path = os.path.join(SCRIPT_DIR, "facebook_volume.py")
                    volume_percent = get_facebook_volume()
                    volume_scalar = convert_to_scalar(volume_percent)
                    subprocess.Popen(["python", script_path, str(volume_scalar)])
                    
            except Exception as e:
                print(f"🔵 Hiba: {e}")
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'OK')

def get_youtube_volume():
    """YouTube hangerő lekérése parancssori argumentumból (0-100)"""
    if len(sys.argv) > 1:
        try:
            volume = int(sys.argv[1])
            volume = max(0, min(100, volume))
            print(f"🔵 YouTube hangerő: {volume}% (paraméterből)")
            return volume
        except ValueError:
            print(f"🔵 Hibás hangerő paraméter: {sys.argv[1]}, alapértelmezett használata: {DEFAULT_YOUTUBE_VOLUME}%")
            return DEFAULT_YOUTUBE_VOLUME
    else:
        print(f"🔵 YouTube hangerő: {DEFAULT_YOUTUBE_VOLUME}% (alapértelmezett)")
        return DEFAULT_YOUTUBE_VOLUME

def get_facebook_volume():
    """Facebook hangerő lekérése parancssori argumentumból (0-100)"""
    if len(sys.argv) > 2:
        try:
            volume = int(sys.argv[2])
            volume = max(0, min(100, volume))
            print(f"🔵 Facebook hangerő: {volume}% (paraméterből)")
            return volume
        except ValueError:
            print(f"🔵 Hibás hangerő paraméter: {sys.argv[2]}, alapértelmezett használata: {DEFAULT_FACEBOOK_VOLUME}%")
            return DEFAULT_FACEBOOK_VOLUME
    else:
        print(f"🔵 Facebook hangerő: {DEFAULT_FACEBOOK_VOLUME}% (alapértelmezett)")
        return DEFAULT_FACEBOOK_VOLUME

if __name__ == "__main__":
    print("🚀 Szerver fut a localhost:8888 porton")
    print(f"📺 YouTube alapértelmezett hangerő: {DEFAULT_YOUTUBE_VOLUME}%")
    print(f"📘 Facebook alapértelmezett hangerő: {DEFAULT_FACEBOOK_VOLUME}%")
    print("\n💡 Használat: python server.py [youtube_volume] [facebook_volume]")
    print(f"📝 Példa: python server.py 50 80")
    print("   (YouTube 50%, Facebook 80%)")
    print("   A hangerő 0-100 között adható meg!\n")
    
    HTTPServer(("0.0.0.0", 8888), RequestHandler).serve_forever()