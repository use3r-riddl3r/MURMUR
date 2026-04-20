#!/usr/bin/env python3
"""
Объединить глобальные камеры наблюдения OSM с существующими данными FLOCK
Преобразует формат OSM в GeoJSON и удаляет дубликаты
"""

import json
from pathlib import Path
from collections import defaultdict

def osm_to_geojson(osm_data):
    """Преобразовать формат OSM в GeoJSON FeatureCollection"""
    features = []

    for element in osm_data.get('elements', []):
        if element.get('type') != 'node':
            continue
        if 'lat' not in element or 'lon' not in element:
            continue

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [element['lon'], element['lat']]
            },
            'properties': element.get('tags', {})
        }
        features.append(feature)

    return features

def main():
    print("="*60)
    print("ОБЪЕДИНЕНИЕ ГЛОБАЛЬНЫХ КАМЕР НАБЛЮДЕНИЯ OSM")
    print("="*60)

    # Загрузить существующие камеры
    print("\nЗагрузка существующих камер FLOCK...")
    with open('CAMERAS_WITH_NETWORK_DATA.geojson', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    print(f"Текущие камеры: {len(existing_data['features']):,}")

    # Создать справочник для удаления дубликатов (по координатам, округленным до 4 знаков)
    existing_coords = set()
    for feat in existing_data['features']:
        lon, lat = feat['geometry']['coordinates']
        coord_key = f"{lat:.4f},{lon:.4f}"
        existing_coords.add(coord_key)

    print(f"Уникальные ключи координат: {len(existing_coords):,}")

    # Загрузить и объединить региональные файлы OSM
    osm_dir = Path('data/raw_osm_global')
    osm_files = sorted(osm_dir.glob('osm_surveillance_*.json'))

    print(f"\nНайдено {len(osm_files)} региональных файлов OSM")

    new_features = []
    duplicates = 0

    for osm_file in osm_files:
        region = osm_file.stem.replace('osm_surveillance_', '').split('_')[0]
        print(f"\nОбработка {region}...")

        with open(osm_file, 'r', encoding='utf-8') as f:
            osm_data = json.load(f)

        features = osm_to_geojson(osm_data)
        print(f"  Сырые камеры: {len(features):,}")

        # Удалить дубликаты
        region_new = 0
        for feat in features:
            lon, lat = feat['geometry']['coordinates']
            coord_key = f"{lat:.4f},{lon:.4f}"

            if coord_key not in existing_coords:
                new_features.append(feat)
                existing_coords.add(coord_key)
                region_new += 1
            else:
                duplicates += 1

        print(f"  Новые камеры: {region_new:,}")
        print(f"  Дубликаты: {len(features) - region_new:,}")

    # Объединить
    print(f"\n{'='*60}")
    print("СВОДКА ПО ОБЪЕДИНЕНИЮ")
    print(f"{'='*60}")
    print(f"Существующие камеры: {len(existing_data['features']):,}")
    print(f"Новые уникальные камеры: {len(new_features):,}")
    print(f"Пропущено дубликатов: {duplicates:,}")
    print(f"Всего после объединения: {len(existing_data['features']) + len(new_features):,}")

    # Объединить
    merged_data = {
        'type': 'FeatureCollection',
        'features': existing_data['features'] + new_features
    }

    # Сохранить объединенный файл
    print(f"\nСохранение объединенных данных...")
    with open('CAMERAS_WITH_NETWORK_DATA.geojson', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f)

    print(f"Сохранено в CAMERAS_WITH_NETWORK_DATA.geojson")

    # Обновить количество камер в сводке
    print(f"\nИтоговое количество камер: {len(merged_data['features']):,}")

    print("\n" + "="*60)
    print("УСПЕХ - Готово к повторной генерации плиток")
    print("="*60)

if __name__ == '__main__':
    main()
