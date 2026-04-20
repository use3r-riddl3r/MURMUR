#!/usr/bin/env python3
"""
Разбить большой GeoJSON на географические плитки для более быстрой загрузки
Создает плитки в каталоге data/tiles/, которые загружаются по требованию
"""

import json
from pathlib import Path
import math

def lat_lon_to_tile(lat, lon, zoom=6):
    """Преобразовать lat/lon в координаты плитки на заданном уровне масштабирования"""
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def create_tiles():
    """Разделить данные камер на географические плитки"""

    print("Loading camera data...")
    with open('CAMERAS_WITH_NETWORK_DATA.geojson', 'r', encoding='utf-8') as f:
        camera_data = json.load(f)

    print(f"Loaded {len(camera_data['features'])} cameras")

    print("\nLoading network data...")
    with open('camera_networks.json', 'r', encoding='utf-8') as f:
        network_data = json.load(f)

    print(f"Loaded {len(network_data)} networks")

    # Создать справочник сетей по местоположению камеры
    network_lookup = {}
    for network in network_data:
        key = f"{network['from'][0]:.4f},{network['from'][1]:.4f}"
        network_lookup[key] = network

    # Хранилище плиток: tiles[zoom][x][y] = {"cameras": [], "networks": []}
    zoom = 6  # Уровень масштабирования 6 = ~64 плитки, покрывающие мир, хороший баланс
    tiles = {}

    print(f"\nСоздание плиток на уровне масштабирования {zoom}...")

    # Распределить камеры на плитки
    for feature in camera_data['features']:
        lon, lat = feature['geometry']['coordinates']
        x, y = lat_lon_to_tile(lat, lon, zoom)

        tile_key = f"{zoom}/{x}/{y}"
        if tile_key not in tiles:
            tiles[tile_key] = {
                'type': 'FeatureCollection',
                'features': [],
                'networks': []
            }

        tiles[tile_key]['features'].append(feature)

        # Добавить данные сети, если они существуют
        cam_key = f"{lat:.4f},{lon:.4f}"
        if cam_key in network_lookup:
            tiles[tile_key]['networks'].append(network_lookup[cam_key])

    # Сохранить плитки в каталог data/tiles/
    tiles_dir = Path('data/tiles')
    tiles_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nСохранение {len(tiles)} плиток...")

    tile_index = {
        'zoom': zoom,
        'tiles': {},
        'total_cameras': len(camera_data['features'])
    }

    for tile_key, tile_data in tiles.items():
        zoom_str, x_str, y_str = tile_key.split('/')

        # Создать структуру каталога: data/tiles/6/x/y.json
        tile_dir = tiles_dir / zoom_str / x_str
        tile_dir.mkdir(parents=True, exist_ok=True)

        tile_file = tile_dir / f"{y_str}.json"

        with open(tile_file, 'w', encoding='utf-8') as f:
            json.dump(tile_data, f)

        # Добавить в индекс
        tile_index['tiles'][tile_key] = {
            'cameras': len(tile_data['features']),
            'networks': len(tile_data['networks']),
            'path': f"data/tiles/{tile_key}.json"
        }

        print(f"  {tile_key}: {len(tile_data['features'])} cameras, {len(tile_data['networks'])} networks")

    # Сохранить индекс плиток
    index_file = tiles_dir / 'index.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(tile_index, f, indent=2)

    print(f"\n✅ Создание плиток завершено!")
    print(f"📁 Плитки сохранены в: {tiles_dir}")
    print(f"📊 Всего плиток: {len(tiles)}")
    print(f"📋 Индекс плиток: {index_file}")

    # Рассчитать средний размер плитки
    total_size = sum(len(json.dumps(t)) for t in tiles.values())
    avg_size = total_size / len(tiles) / 1024  # КБ
    print(f"📦 Средний размер плитки: {avg_size:.1f} КБ")
    print(f"💾 Общий размер данных: {total_size / 1024 / 1024:.1f} МБ")

    print(f"\n🚀 Следующий шаг: обновить index.html для использования загрузки на основе плиток")

if __name__ == '__main__':
    create_tiles()
