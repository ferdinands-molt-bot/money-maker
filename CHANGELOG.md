# Changelog

All notable changes to ContentMultiplier will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-07

### Added - Major Features
- **10 Platform Support** (expanded from 6)
  - Added TikTok with viral script generation
  - Added Pinterest with SEO-optimized descriptions
  - Added Threads for Meta's text platform
  - Added Reddit for community engagement
  - All platforms now include engagement score predictions

- **Enhanced UI/UX**
  - Word count display alongside character count
  - Estimated reading time calculation
  - Animated progress bar during content generation
  - Keyboard shortcuts modal (? key)
  - Select All / Deselect All platform buttons
  - Improved copy-to-clipboard with visual feedback

- **Export & Download Features**
  - Download All results as text file
  - Export results as structured JSON
  - Copy All results to clipboard
  - Clear All results button

- **History & Storage**
  - LocalStorage-based conversion history
  - Automatic saving of last 20 conversions
  - Persistent history across sessions

- **Enhanced Content Generation**
  - Tone-specific hooks for each platform
  - Platform-optimized formatting
  - Engagement predictions for each platform
  - Character count warnings

- **Developer Experience**
  - Comprehensive keyboard shortcuts (Ctrl+Enter, Ctrl+A, Ctrl+D, ?)
  - Improved error handling
  - Better analytics tracking
  - Updated documentation

### Changed
- Updated all references from "6 platforms" to "10 platforms"
- Improved landing page with all 10 platform showcases
- Enhanced demo endpoint to show all platforms
- Updated pricing to reflect 10 platforms
- Refined UI with better animations and transitions

### Technical Improvements
- Enhanced server.py with 4 new platform generators
- Improved JavaScript with modular functions
- Added CSS animations and tooltips
- Better responsive design

---

## [1.0.0] - 2026-02-07

### Added
- Initial MVP release
- Content conversion for 6 platforms (Twitter, LinkedIn, Instagram, Facebook, YouTube, Newsletter)
- Web interface with Tailwind CSS
- REST API with Flask
- Pricing plans (Free, Pro $9/mo, Business $29/mo)
- Docker support with Dockerfile and docker-compose.yml
- Comprehensive documentation:
  - README.md with quick start
  - API.md with endpoint documentation
  - DEPLOYMENT.md for production deployment
  - MONETIZATION.md for revenue strategies
  - MARKETING_KIT.md with copy and templates
  - QUICKSTART.md for immediate monetization
  - CONTRIBUTING.md for contributors
  - ROADMAP.md for future plans
- GitHub Actions CI/CD pipeline
- Issue and PR templates
- MIT License

### Features
- Real-time content conversion
- Multiple tone options (professional, casual, enthusiastic, educational, witty)
- Platform selection interface
- Copy-to-clipboard functionality
- Character counting
- Demo mode
- Responsive design

### Technical
- Python Flask backend
- Vanilla JavaScript frontend
- Static file serving
- CORS support
- JSON API responses

---

## Version History

- v2.0.0 (2026-02-07) - Major Update: 10 Platforms, Enhanced UI, Export Features
- v1.0.0 (2026-02-07) - Initial MVP Launch
