"""HTML generation for My History panel - Device column version, no state, with tooltips."""
from datetime import datetime
from .css import CSS_STYLES
from .javascript import JAVASCRIPT_CODE

def generate_panel_html(entities, devices, device_names, tracked, purge_days):
    """Generate complete HTML for the panel."""
    
    # Build device dropdown options
    device_options = ""
    for device in sorted(devices, key=lambda d: d.name_by_user or d.name or ""):
        device_name = device.name_by_user or device.name or "Unnamed Device"
        if device.id:
            device_options += f'<option value="{device.id}">{device_name}</option>\n'
    
    # Build entity table rows with device as separate column - NO STATE
    rows = _generate_entity_rows(entities, tracked)
    
    # Get current time
    current_time = datetime.now().strftime('%H:%M:%S')
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>My History - Entity Exclusions</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{CSS_STYLES}</style>
</head>
<body>
    <div class="container">
        {_generate_header(current_time)}
        {_generate_filter_bar(entities, device_options)}
        {_generate_retention_settings(purge_days)}
        {_generate_entity_table(rows)}
        {_generate_config_guide()}
    </div>

    <script>{JAVASCRIPT_CODE}</script>
</body>
</html>"""

def _generate_entity_rows(entities, tracked):
    """Generate table rows for entities - NO STATE column."""
    rows = ""
    
    for entity in entities:
        checked = "checked" if entity["selected"] else ""
        device_id = entity["device_id"] or ""
        device_name = entity["device_name"]
        entity_id = entity["entity_id"]
        
        rows += f"""
        <tr data-device-id="{device_id}" data-entity-id="{entity_id}">
            <td class="device-cell">
                <span class="device-name" title="Device ID: {device_id if device_id else 'No device'}">{device_name}</span>
            </td>
            <td class="entity-cell">
                <div class="entity-name">
                    <span class="entity-friendly" title="Entity ID: {entity_id}">{entity['name']}</span>
                </div>
            </td>
            <td class="checkbox-cell">
                <input type="checkbox" class="entity-checkbox" 
                       data-entity-id="{entity_id}"
                       {checked}>
            </td>
        </tr>
        """
    
    if not rows:
        rows = """
        <tr>
            <td colspan="3" class="empty-state">
                <div class="empty-message">
                    <span class="empty-icon">📊</span>
                    <h3>No entities found</h3>
                </div>
            </td>
        </tr>
        """
    
    return rows

def _generate_header(current_time):
    """Generate header section."""
    return f"""
    <div class="header">
        <h1>My History - Entity Exclusions</h1>
        <div class="header-controls">
            <span class="last-updated">Last updated: {current_time}</span>
            <button class="refresh-btn" onclick="location.reload()">⟳ Refresh</button>
        </div>
    </div>
    """

def _generate_filter_bar(entities, device_options):
    """Generate filter bar section."""
    return f"""
    <div class="filter-bar">
        <label for="device-filter">Filter by device:</label>
        <select id="device-filter" onchange="filterByDevice(this.value)">
            <option value="">All Devices ({len(entities)})</option>
            {device_options}
        </select>
        <div class="stats" id="visible-count">Showing all entities</div>
    </div>
    """

def _generate_retention_settings(purge_days):
    """Generate retention settings card."""
    return f"""
    <div class="card">
        <h2>Data Retention Settings</h2>
        <div class="setting-row">
            <label for="purge-days">Days to keep history:</label>
            <input type="number" id="purge-days" min="1" max="365" value="{purge_days}">
            <small>Excluded entities will be purged after this many days</small>
        </div>
    </div>
    """

def _generate_entity_table(rows):
    """Generate entity table card - NO STATE column."""
    return f"""
    <div class="card">
        <h2>Entities to Exclude from History</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th class="device-header">Device</th>
                        <th class="entity-header">Entity</th>
                        <th class="checkbox-header">Exclude</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        
        <div class="action-bar">
            <div class="select-all">
                <input type="checkbox" id="select-all" onchange="toggleAll(this)">
                <label for="select-all">Select All Visible</label>
            </div>
            <button class="save-btn" onclick="saveSelections()">Save Exclusions</button>
        </div>
    </div>
    """

def _generate_config_guide():
    """Generate configuration guide card."""
    return """
    <div class="card">
        <h2>📝 One-Line Integration</h2>
        <p>Add this single line to your <code>configuration.yaml</code>:</p>
        
        <div style="background: var(--gray-light); padding: 12px; border-radius: 6px; margin: 12px 0; position: relative;">
            <pre style="margin: 0; font-size: 13px;">recorder: !include recorder_config.yaml</pre>
            <button onclick="copyConfigLine()" style="position: absolute; top: 8px; right: 8px; padding: 4px 8px; background: var(--primary-color); color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">📋 Copy</button>
        </div>
        
        <p>Your <code>recorder_config.yaml</code> will be automatically generated.</p>
        
        <div style="background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 10px; border-radius: 6px; font-size: 13px;">
            <strong>✅</strong> After adding the line, restart Home Assistant.
        </div>
    </div>

    <script>
    function copyConfigLine() {
        const text = 'recorder: !include recorder_config.yaml';
        navigator.clipboard.writeText(text).then(() => {
            alert('✅ Copied to clipboard!');
        });
    }
    </script>
    """