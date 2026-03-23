# My History for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![HACS][hacs-shield]][hacs]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

**A custom integration that provides a user-friendly sidebar panel to manage which entities are excluded from Home Assistant's history/recorder database.**

## 📖 Overview

My History gives you a simple web interface to control what gets stored in your Home Assistant database. Instead of manually editing `configuration.yaml` and restarting, you can:

- **Exclude entities** from being recorded
- **Set purge retention days** per entity
- **Save changes instantly** without restarts

The integration generates a `recorder_config.yaml` file automatically and integrates seamlessly with Home Assistant's built-in recorder component.

## ✨ Features

- 🖥️ **Sidebar Panel** - A clean web interface accessible from your Home Assistant sidebar
- 📝 **Entity Exclusion** - Select which entities should NOT be recorded in history
- ⏱️ **Purge Control** - Set how many days of history to keep for excluded entities
- ⚡ **No Restart Required** - Changes take effect immediately
- 🔧 **Auto-Generated Config** - Creates and updates `recorder_config.yaml` automatically
- 🎯 **Works with Recorder** - Fully compatible with Home Assistant's native recorder component

## 📦 Installation

### HACS Installation (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed
2. Open HACS → Integrations
3. Click the three dots → Custom repositories
4. Add `https://github.com/RadioactiveMan56/my_history` (Category: Integration)
5. Click "Install" on My History
6. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page][releases]
2. Copy the `my_history` folder to `/config/custom_components/`
3. Restart Home Assistant

## ⚙️ Configuration

### Initial Setup

After installation:

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for "My History"
4. Complete the configuration flow:
   - Select entities to exclude from history (optional initially)
   - Set purge retention days (default: 30)

### Configuration Options

The integration stores settings in `recorder_config.yaml`:

```yaml
purge_keep_days: 30
exclude:
  entities:
    - sensor.uptime
    - sensor.last_boot
    - binary_sensor.*_battery
