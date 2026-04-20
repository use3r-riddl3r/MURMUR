# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2024-04-20 (Initial Release)

### Added

#### Core Features
- **Country-based map loading** — Select any country to load only that region's cameras (fixes original FLOCK memory crash)
- **Global camera coverage** — 336,708+ surveillance cameras from multiple sources
- **UK TfL JamCam integration** — 1,000+ live London traffic camera feeds with thumbnails
- **France national dataset** — CCTV data from data.gouv.fr
- **Network visualization** — Draw data-sharing lines between Flock Safety and partner agencies
- **OSINT toolkit** — Pre-filled searches on Shodan, ZoomEye, FOFA, Insecam, Google Dorks

#### Technical
- 12-module clean JavaScript architecture (CONFIG, STATE, UTILS, MARKERS, SOURCES, NETWORK, COUNTRY, UI, SEARCH, APP, POPUP, LOADER)
- Proper async/await throughout (no setTimeout hacks)
- Responsive design — Mobile and desktop support
- Geographic tile system (zoom level 6) for efficient data loading
- GeoJSON FeatureCollection format with network metadata

#### Data Sources
- OpenStreetMap surveillance data (community-contributed)
- TfL Unified API (UK live feeds)
- data.gouv.fr (France national dataset)
- EFF Atlas of Surveillance (identified, ready for integration)
- McClatchy Private Eyes (identified, ready for integration)

### Fixed
- ✓ Browser crash when loading all 336K cameras at once (now country-based)
- ✓ Character encoding issues with European operator names (accented characters in btoa())
- ✓ Map animation timing issues (removed setTimeout hacks, proper async/await)
- ✓ Variable re-declaration in loops

### Changed
- Refactored entire codebase from original FLOCK into 12 clean modules
- Replaced Shodan-only OSINT with free/open alternatives (ZoomEye, FOFA, Insecam, Google Dorks)
- Expanded scope from US-only to global coverage with regional data sources

### Documentation
- Complete README with features, camera types, quick start
- Comprehensive DEPLOY.md with GitHub Pages instructions and troubleshooting
- DATA_SOURCES.md detailing 7 data sources with integration status
- Inline code comments for module architecture
- MIT license with data attribution

---

## [Unreleased] - Future Enhancements

### Planned
- [ ] EFF Atlas integration (automated import)
- [ ] McClatchy agency ALPR data integration
- [ ] Monthly automated data refresh workflow
- [ ] Contributing guidelines for camera data submissions
- [ ] Google Analytics integration (optional)
- [ ] Desktop app wrapper (Electron)
- [ ] API for programmatic access
- [ ] Slack/Discord webhook alerts for new cameras

### Under Consideration
- [ ] WebGL rendering for 1000+ network lines (performance)
- [ ] 3D map view (Cesium.js)
- [ ] Real-time camera feed quality/availability checker
- [ ] Community flagging system (for moved/removed cameras)
- [ ] Historical camera data (what was there X months ago)
- [ ] Camera feeding status verification

---

## Notes

### Original Project
Built on foundation of [ringmast4r's FLOCK](https://github.com/ringmast4r/FLOCK)
- Concept: Map Flock Safety network in United States
- Original data: ~178K+ US-based cameras
- This version (MURMUR) expands globally and integrates additional data sources

### Versioning Strategy
- **Major version** (X.0.0): Breaking changes or major feature additions
- **Minor version** (0.X.0): New features, backwards compatible
- **Patch version** (0.0.X): Bug fixes, minor updates

### Data Freshness
- Camera data: Updated on request (manual re-run of `merge_osm_global.py`)
- TfL JamCam feeds: Real-time (live API)
- France CCTV data: Synced when available on data.gouv.fr
- Network relationships: Updated when camera data refreshed

---

## Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

See CONTRIBUTING.md (coming soon) for detailed guidelines.

---

## License

MIT License - See LICENSE file for details.

Data sources retain their original licenses (ODbL for OSM, Licence Ouverte for data.gouv.fr, etc.)

---

## Support

- 📖 **Documentation**: See README.md and DEPLOY.md
- 🐛 **Bug Reports**: Open issue on GitHub
- 💬 **Discussions**: GitHub Discussions tab
- 🌐 **Community**: r/privacy, r/dataisbeautiful on Reddit

