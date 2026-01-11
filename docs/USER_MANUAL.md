# PyCountdown User Manual

A comprehensive guide to using PyCountdown, a powerful countdown clock application for managing multiple customizable timers and clocks.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Main Interface](#main-interface)
5. [Working with Clocks](#working-with-clocks)
6. [Clock Editor](#clock-editor)
7. [Timers](#timers)
8. [Threshold Sets](#threshold-sets)
9. [Configuration Files](#configuration-files)
10. [Time Formats](#time-formats)
11. [Time Rates](#time-rates)
12. [Program Configuration](#program-configuration)
13. [Keyboard Shortcuts](#keyboard-shortcuts)
14. [Clocks File Format (JSON Schema)](#clocks-file-format-json-schema)
15. [Advanced Topics](#advanced-topics)
16. [Troubleshooting](#troubleshooting)

---

## Introduction

PyCountdown is a desktop application for displaying and managing multiple countdown timers and clocks. It supports:

- Multiple simultaneous countdown timers
- Absolute time clocks in various time scales (UTC, TAI, GPS Time, etc.)
- US timezone clocks with DST handling
- Customizable display formats
- Color-coded thresholds for visual alerts
- Persistent clock configurations via JSON files
- Always-on-top window mode with opacity control

PyCountdown is built on the PyRandyOS framework and uses PySide2 (Qt) for its graphical interface.

---

## Installation

### Requirements

- Python 3.10 or later
- PySide2
- pyrandyos (dependency)

### Installing from PyPI

```bash
pip install PyCountdown
```

### Installing from Source

```bash
git clone https://github.com/emanspeaks/pycountdown.git
cd pycountdown
pip install -e .
```

### Optional Dependencies

For dark theme support:
```bash
pip install PyCountdown[qdarkstyle]
```

---

## Getting Started

### Launching PyCountdown

Run PyCountdown from the command line:

```bash
python -m pycountdown
```

On first launch, PyCountdown will create a default configuration. You can specify a clocks file:

```bash
python -m pycountdown /path/to/clocks.jsonc
```

### First Steps

1. **Create your first clock**: Click the "Add clock" button in the toolbar
2. **Create a timer**: Click the "Add timer" button for a quick countdown
3. **Save your configuration**: Use "Save Clocks file as..." to persist your clocks

---

## Main Interface

The main window displays your clocks in a table format with a toolbar for common actions.

![Main Window](images/main_window.png)

### Toolbar

![Toolbar](images/toolbar.png)

The toolbar provides quick access to all major functions (left to right):

| Action | Description |
|--------|-------------|
| **Add clock** | Opens the clock editor to create a new clock |
| **Remove clock** | Deletes selected clock(s) after confirmation |
| **Add timer** | Creates a new countdown timer from the current time |
| **Move up** | Moves selected clock(s) up in the list |
| **Move down** | Moves selected clock(s) down in the list |
| **Duplicate** | Creates a copy of selected clock(s) |
| **Show hidden** | Toggles visibility of hidden clocks |
| **Threshold Sets** | Opens the threshold set editor |
| **Apply Threshold Set** | Applies a threshold set to selected clocks |
| **Refresh** | Reloads the clocks file from disk |
| **New** | Creates a new empty clocks configuration |
| **Open** | Opens an existing clocks file |
| **Save As** | Saves the current configuration to a new file |
| **Clocks config** | Opens the raw JSON configuration editor |
| **Program config** | Opens the program settings viewer |

### Clock Table

The main display shows all clocks in a two-column table:

- **Clock column**: Displays the label/name of each clock
- **Current Time column**: Shows the live time value, updated every second

#### Selecting Clocks

- Click a row to select a single clock
- Hold Ctrl and click to select multiple clocks
- Hold Shift and click to select a range of clocks

#### Editing Clocks

- Double-click any row to open the clock editor for that clock
- Click the row header (row number) to open the clock editor

---

## Working with Clocks

### Understanding Clock Types

PyCountdown supports several types of clocks:

1. **Absolute Clocks**: Display the current time in a specific time scale
2. **Countdown/Countup Clocks**: Count relative to a specific epoch (target time)
3. **Following Clocks**: Clocks that follow another clock with an optional offset
4. **Blank Rows**: Empty rows used for visual separation

### Built-in Default Clocks

PyCountdown includes these pre-defined clocks that can be referenced:

| Clock ID | Description |
|----------|-------------|
| UTC | Coordinated Universal Time |
| TAI | International Atomic Time |
| TT / TDT | Terrestrial Time (Terrestrial Dynamical Time) |
| T_eph / TDB | Ephemeris Time / Barycentric Dynamical Time |
| US ET | US Eastern Time (with DST) |
| US CT | US Central Time (with DST) |
| US MT | US Mountain Time (with DST) |
| US PT | US Pacific Time (with DST) |
| GPST | GPS Time |
| Unix | Unix timestamp |

### Creating a New Clock

1. Click **Add clock** in the toolbar
2. Fill in the clock properties:
   - **Label**: Display name for the clock
   - **Clock ID**: Optional unique identifier (defaults to label)
   - **Epoch**: The reference time point
   - **Reference**: Optional real-time reference for offset calculations
   - **Follow**: Optional clock to follow/mirror
   - **Tick rate**: Time scale for the clock
   - **Display options**: Formatting and visibility settings
3. Click **OK** to create the clock

### Editing an Existing Clock

1. Double-click the clock row, or click the row header
2. Modify the desired properties
3. Click **OK** to save changes, or **Cancel** to discard

### Removing Clocks

1. Select one or more clocks
2. Click **Remove clock** in the toolbar
3. Confirm the deletion in the dialog

### Reordering Clocks

1. Select one or more clocks
2. Click **Move up** or **Move down** to reposition
3. Changes are saved automatically

### Duplicating Clocks

1. Select one or more clocks
2. Click **Duplicate** or press **Ctrl+D**
3. A copy is created immediately below each selected clock

---

## Clock Editor

The clock editor dialog allows complete control over clock properties.

![Clock Editor](images/clock_editor.png)

### Label and ID

- **Label**: The display name shown in the clock table
- **Blank**: Check to create a blank separator row (ignores other settings except label)
- **Clock ID**: A unique identifier used to reference this clock from other clocks. If unchecked, the label is used as the ID.

### Epoch Settings

The epoch defines the reference point for the clock:

- **Epoch checkbox**: Enable/disable epoch specification
- **Clock reference**: Select which clock the epoch time is relative to (e.g., UTC, TAI)
- **Time value**: The epoch time in the selected format
- **Format**: How the time value is interpreted (seconds, DHMS, YMDHMS, etc.)
- **Fold options**: For handling ambiguous times during DST transitions

#### Epoch Examples

| Epoch | Clock | Meaning |
|-------|-------|---------|
| `[2025, 1, 1, 0, 0, 0]` | UTC | January 1, 2025 00:00:00 UTC |
| `3600` | TAI | 3600 seconds after TAI epoch |
| `[-5, 12, 30, 0]` | UTC | 5 days, 12 hours, 30 minutes before now |

### Real-time Reference

For offset clocks, the reference defines when the epoch time should match real-time:

- When enabled, the clock displays time relative to the difference between epoch and reference
- Useful for creating clocks that show "time since event" or "time until event"

### Follow Clock

- Enable to make this clock follow another clock's time
- The followed clock's offset and rate are inherited
- Useful for creating clocks that track the same event with different display formats

### Tick Rate

Select the time scale for the clock:

- **TAI**: International Atomic Time (default)
- **UTC**: Coordinated Universal Time
- **UNIX**: Unix time (seconds since 1970-01-01 UTC)
- **TT**: Terrestrial Time
- **T_EPH**: Ephemeris Time
- **US_ET/CT/MT/PT**: US timezone rates with DST

### Display Options

#### Hidden

Check to hide the clock from the main display. Hidden clocks can still be referenced by other clocks. Use "Show hidden" in the toolbar to reveal them.

#### Decimal Digits

Number of decimal places to show for seconds (0-20).

#### Zero-padded Width

Minimum width for the integer portion, padded with leading zeros.

#### Display Format

How the time is displayed:

| Format | Example | Description |
|--------|---------|-------------|
| S | `86400` | Seconds only |
| M | `1440.0` | Minutes only |
| H | `24.0` | Hours only |
| D | `1.0` | Days only |
| DHMS | `1d 00:00:00` | Days, hours, minutes, seconds |
| Y_DOY_HMS | `2025/001 00:00:00` | Year, day-of-year, time |
| YMDHMS | `2025-01-01 00:00:00` | Full date and time |

#### Threshold Set

Select a threshold set to apply color-based styling. See [Threshold Sets](#threshold-sets).

#### Default Color

Click to choose the default text color for this clock.

---

## Timers

Timers are simplified clocks designed for quick countdowns.

![Timer Editor](images/timer_editor.png)

### Creating a Timer

1. Click **Add timer** in the toolbar
2. Enter a **Label** for the timer
3. Set the **Epoch** (countdown target time)
4. Configure display options
5. Click **OK**

### Timer vs Clock

Timers differ from clocks in that:

- They automatically use the current time as reference
- They don't have follow/rate options
- They're designed for quick countdown creation

### Timer Display

- **Negative values**: Time remaining until the epoch (countdown)
- **Positive values**: Time elapsed since the epoch (countup)

---

## Threshold Sets

Threshold sets enable dynamic color-coding based on time values.

![Threshold Sets Editor](images/threshold_sets_editor.png)

### Understanding Thresholds

A threshold set is a list of thresholds, each defining:
- An **epoch** (time value)
- A **color** to display when the clock time reaches that threshold

The clock displays the color of the most recent threshold (chronologically) that has been reached.

### Creating and Managing Threshold Sets

1. Click **Threshold Sets** in the toolbar
2. Use **Add set** to create a new threshold set
3. Enter a name for the set
4. Add thresholds using **Add threshold**
5. For each threshold:
   - Set the epoch (time value) or leave blank for default
   - Choose a color
   - Click **Update threshold** to save
6. Click **Save** or **OK** when done

### Threshold Set Example

Create a countdown warning system:

| Threshold Epoch | Color | Meaning |
|-----------------|-------|---------|
| (none/default) | White | Default color |
| -300 seconds | Yellow | 5 minutes remaining |
| -60 seconds | Orange | 1 minute remaining |
| -10 seconds | Red | 10 seconds remaining |
| 0 seconds | Green | Time reached |

### Applying Threshold Sets

![Apply Threshold Set](images/apply_threshold_set.png)

1. Select one or more clocks
2. Click **Apply Threshold Set**
3. Choose the threshold set to apply
4. Click **OK**

Or, in the clock editor:
1. Check **Threshold sets**
2. Select the desired threshold set from the dropdown

---

## Configuration Files

PyCountdown uses JSON/JSONC files for storing clock configurations.

### Clocks File Location

By default, PyCountdown looks for `clocks.jsonc` in the current directory. The file path can be:

- Specified on the command line
- Set in the local configuration
- Selected using File > Open

### File Operations

| Action | Description |
|--------|-------------|
| New | Clears all clocks and starts fresh |
| Open | Loads clocks from a different file |
| Save As | Saves current clocks to a new file |
| Refresh | Reloads the current file from disk |

### Auto-reload

PyCountdown periodically checks the clocks file for changes (every 5 seconds by default) and automatically reloads if modified externally.

### Clocks JSON Editor

For direct access to the JSON configuration:

![Clocks Configuration JSON Editor](images/clocks_config_json.png)

1. Click **Clocks config** in the toolbar
2. Edit the raw JSON data
3. Save changes

---

## Time Formats

PyCountdown supports multiple time formats for input and display.

### Available Formats

| Format | Input Example | Display Example |
|--------|---------------|-----------------|
| **S** (Seconds) | `86400` | `86400` |
| **M** (Minutes) | `1440` | `1440.00` |
| **H** (Hours) | `24` | `24.00` |
| **D** (Days) | `1` | `1.00` |
| **DHMS** | `[1, 12, 30, 45]` | `1d 12:30:45` |
| **Y_DOY_HMS** | `[2025, 1, 12, 30, 45]` | `2025/001 12:30:45` |
| **YMDHMS** | `[2025, 1, 1, 12, 30, 45]` | `2025-01-01 12:30:45` |

### DHMS Format Details

DHMS can be specified as:
- 4-element array: `[days, hours, minutes, seconds]`
- 5-element array: `[days, hours, minutes, seconds, sign]` where sign is -1 or 1
- String with slash: `"1/12:30:45"` or `"-1\12:30:45"`

### Negative Times

For countdown displays, negative values indicate time in the future:
- `-1d 00:00:00` means 1 day until the target
- `1d 00:00:00` means 1 day since the target

---

## Time Rates

Time rates define how a clock's time relates to real-world time.

### Available Rates

| Rate | Description |
|------|-------------|
| **TAI** | International Atomic Time - continuous, no leap seconds |
| **UTC** | Coordinated Universal Time - includes leap seconds |
| **UNIX** | Unix time - seconds since 1970-01-01 UTC |
| **TT** | Terrestrial Time - used in astronomy |
| **T_EPH** | Ephemeris Time / TDB - used in planetary ephemerides |
| **US_ET** | US Eastern Time (with automatic DST) |
| **US_CT** | US Central Time (with automatic DST) |
| **US_MT** | US Mountain Time (with automatic DST) |
| **US_PT** | US Pacific Time (with automatic DST) |

### Rate Inheritance

When a clock follows another:
- If no rate is specified, it inherits the followed clock's rate
- If no follow is specified and no rate is set, TAI is used

---

## Program Configuration

Access program settings via the **Program config** button.

![Program Configuration](images/program_config.png)

### Configuration Viewer

The configuration dialog displays:
- Global configuration settings
- Local (per-machine) configuration settings
- System information (Python paths, environment variables)

### Key Settings

| Setting | Description |
|---------|-------------|
| `clocks_file` | Path to the default clocks file |
| `clocks_file_check_sec` | Interval for checking file changes (default: 5) |
| `local.show_hidden` | Whether hidden clocks are visible |
| `local.always_on_top` | Window stays above other windows |
| `local.always_on_top_opacity` | Window opacity when not focused (0.0-1.0) |
| `local.json_schema` | URL for clocks file JSON schema |

### Saving Configuration

- **Save Local Config**: Saves machine-specific settings
- **Export Full Config**: Exports all configuration to a file

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+D** | Duplicate selected clock(s) |
| **Ctrl+S** | Save (in clock editor dialog) |

---

## Clocks File Format (JSON Schema)

The clocks file is a JSONC (JSON with comments) file with the following structure:

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/emanspeaks/PyCountdown/refs/heads/master/pycountdown/assets/clocks.schema.jsonc",
  "threshold_sets": {
    "warning": [
      { "color": "white" },
      { "epoch": { "t": -300 }, "color": "yellow" },
      { "epoch": { "t": -60 }, "color": "red" },
      { "epoch": { "t": 0 }, "color": "green" }
    ]
  },
  "clocks": [
    {
      "label": "UTC",
      "id": "utc_clock",
      "rate": "UTC",
      "display": {
        "format": "YMDHMS",
        "color": "white"
      }
    },
    {
      "label": "Launch Countdown",
      "epoch": {
        "clock": "UTC",
        "t": [2025, 6, 15, 12, 0, 0],
        "format": "YMDHMS"
      },
      "display": {
        "format": "DHMS",
        "thresholds": "warning"
      }
    },
    {
      "blank": true
    }
  ]
}
```

### Clock Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `label` | string | Display name |
| `id` | string | Unique identifier (optional, defaults to label) |
| `blank` | boolean | If true, creates a blank separator row |
| `epoch` | object | Epoch definition |
| `ref` | object | Reference epoch for offset clocks |
| `follow` | string | ID of clock to follow |
| `rate` | string | Time rate (TAI, UTC, etc.) |
| `display` | object | Display formatting options |

### Epoch Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `clock` | string | Reference clock ID |
| `t` | number/array/string | Time value |
| `format` | string | Time format (S, DHMS, YMDHMS, etc.) |
| `fold_known` | boolean | Whether fold value is explicitly known |
| `fold` | boolean | For DST ambiguity resolution |

### Display Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `hidden` | boolean | Hide from display |
| `format` | string | Display format |
| `digits` | number | Decimal digits for seconds |
| `zeropad` | number | Minimum width with zero-padding |
| `thresholds` | string | Threshold set name |
| `color` | string/array | Default color (name or RGB array) |

---

## Advanced Topics

### Clock Relationships

Clocks can reference each other to create complex timing relationships:

1. **Epoch clock reference**: The epoch time is interpreted relative to another clock
2. **Follow relationship**: One clock mirrors another with inherited properties
3. **Reference offset**: The difference between epoch and reference defines the offset

### Example: Mission Timer

Create a mission timer that counts up from launch:

```jsonc
{
  "label": "Mission Elapsed Time",
  "epoch": {
    "clock": "UTC",
    "t": [2025, 1, 15, 10, 30, 0],
    "format": "YMDHMS"
  },
  "ref": {
    "clock": "UTC",
    "t": [2025, 1, 15, 10, 30, 0],
    "format": "YMDHMS"
  },
  "display": {
    "format": "DHMS",
    "digits": 0
  }
}
```

### Example: Countdown with Multiple Checkpoints

```jsonc
{
  "threshold_sets": {
    "launch_sequence": [
      { "color": "white" },
      { "epoch": { "t": -3600 }, "color": "#88FF88" },
      { "epoch": { "t": -600 }, "color": "yellow" },
      { "epoch": { "t": -60 }, "color": "orange" },
      { "epoch": { "t": -10 }, "color": "red" },
      { "epoch": { "t": 0 }, "color": "lime" }
    ]
  }
}
```

### Window Always-on-Top

Configure the window to stay on top with reduced opacity when inactive:

1. Set `local.always_on_top` to `true` in configuration
2. Set `local.always_on_top_opacity` to a value between 0.0 and 1.0

---

## Troubleshooting

### Using the Log History

When diagnosing issues, the Log History provides detailed information about application events, errors, and configuration loading. Access it through the application's logging features.

![Log History](images/log_history.png)

The Log History displays:
- **Timestamp**: When each event occurred
- **Level**: Severity level (DEBUG, INFO, WARNING, ERROR)
- **File**: Source code file where the event originated
- **Function**: The function that generated the log entry
- **Message**: Detailed description of the event

Use the log history to:
- Identify configuration file parsing errors
- Track clock file reload events
- Debug theme and UI initialization issues
- Monitor application startup sequence

### Clock Not Updating

- Check that the clock has a valid epoch or is not blank
- Verify the referenced clocks exist
- Refresh from file to reload configuration
- Check the log history for any parsing errors

### Colors Not Changing

- Verify threshold set is assigned to the clock
- Check threshold epoch values are in the expected range
- Ensure thresholds are in chronological order
- Verify the threshold set name matches exactly (case-sensitive)

### File Not Loading

- Verify JSON syntax is correct (use a JSON validator)
- Check file path is accessible
- Look for error messages in the status bar
- Review the log history for detailed error messages

### Clock Shows Wrong Time

- Verify the correct time rate is selected
- Check epoch and reference values
- Ensure the reference clock ID exists
- Verify DST settings if using US timezone rates

### Application Won't Start

- Verify Python 3.10+ is installed
- Check PySide2 is installed correctly
- Ensure pyrandyos dependency is available
- Check the log file in `~/pycountdown/logs/` for startup errors

### Common Log Messages

| Message | Meaning |
|---------|---------|
| `clocks file reloaded` | Configuration file was successfully loaded |
| `Clock not found: <name>` | A referenced clock ID doesn't exist |
| `Unresolved clocks` | Circular dependency or missing reference in clock definitions |

---

## Support

- **Issues**: https://github.com/emanspeaks/pycountdown/issues
- **Source**: https://github.com/emanspeaks/pycountdown

---

*PyCountdown - Countdown clocks made easy*
