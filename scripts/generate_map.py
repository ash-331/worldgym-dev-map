import os
import gpxpy
import folium
import json
from geopy.geocoders import Nominatim
from pathlib import Path

# 設定地圖中心點
geolocator = Nominatim(user_agent="gpx-map")
location = geolocator.geocode("新北市新莊區民安路188巷5號")
map_center = [location.latitude, location.longitude]

# 建立 Folium 地圖
m = folium.Map(location=map_center, zoom_start=15)

# 載入 GPX 檔案
folder = '2025-08'
for file in os.listdir(folder):
    if file.endswith('.gpx'):
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    points = [(point.latitude, point.longitude) for point in segment.points]
                    folium.PolyLine(points, color="blue", weight=5).add_to(m)

# 標記主要位置
folium.Marker(
    location=map_center,
    popup="新莊 WorldGym",
    icon=folium.Icon(color="green", icon="home")
).add_to(m)

# 輸出 HTML
output_dir = Path(folder)
output_dir.mkdir(exist_ok=True)
m.save(output_dir / "index.html")
