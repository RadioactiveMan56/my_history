"""Compact CSS styles for My History panel - Optimized column widths."""
CSS_STYLES = """
:root {
    --primary-color: #03a9f4;
    --primary-dark: #0288d1;
    --success-color: #4caf50;
    --warning-color: #ff9800;
    --danger-color: #f44336;
    --gray-light: #f5f5f5;
    --gray: #9e9e9e;
    --text-primary: #212121;
    --text-secondary: #757575;
    --divider: #e0e0e0;
    --card-bg: #ffffff;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--gray-light);
    color: var(--text-primary);
    line-height: 1.4;
    padding: 12px;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
}

/* Compact header */
.header {
    background: var(--card-bg);
    border-radius: 8px;
    box-shadow: var(--shadow);
    padding: 10px 16px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}

.header h1 {
    font-size: 18px;
    font-weight: 500;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

.header h1:before {
    content: "📊";
    font-size: 20px;
}

.header-controls {
    display: flex;
    align-items: center;
    gap: 10px;
}

.last-updated {
    color: var(--text-secondary);
    font-size: 12px;
}

.refresh-btn {
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: opacity 0.2s;
}

.refresh-btn:hover {
    opacity: 0.8;
}

/* Compact filter bar */
.filter-bar {
    background: var(--card-bg);
    border-radius: 8px;
    box-shadow: var(--shadow);
    padding: 8px 12px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.filter-bar label {
    font-weight: 500;
    color: var(--text-secondary);
    font-size: 13px;
}

.filter-bar select {
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid var(--divider);
    background: var(--card-bg);
    color: var(--text-primary);
    font-size: 13px;
    min-width: 200px;
}

.stats {
    margin-left: auto;
    color: var(--text-secondary);
    font-size: 12px;
}

/* Compact cards */
.card {
    background: var(--card-bg);
    border-radius: 8px;
    box-shadow: var(--shadow);
    padding: 12px 16px;
    margin-bottom: 12px;
}

.card h2 {
    font-size: 15px;
    font-weight: 500;
    margin: 0 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--divider);
    display: flex;
    align-items: center;
    gap: 6px;
}

.card h2:before {
    content: "📌";
    font-size: 16px;
}

/* Compact setting row */
.setting-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
    flex-wrap: wrap;
}

.setting-row label {
    font-weight: 500;
    color: var(--text-secondary);
    min-width: 100px;
    font-size: 13px;
}

.setting-row input[type="number"] {
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid var(--divider);
    background: var(--card-bg);
    color: var(--text-primary);
    font-size: 13px;
    width: 70px;
}

.setting-row small {
    color: var(--text-secondary);
    font-size: 11px;
}

/* Compact table - optimized column widths */
.table-container {
    overflow-x: auto;
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid var(--divider);
    border-radius: 6px;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    table-layout: fixed;
}

th {
    text-align: left;
    padding: 8px 6px;
    background: var(--gray-light);
    color: var(--text-primary);
    font-weight: 500;
    font-size: 12px;
    position: sticky;
    top: 0;
    z-index: 10;
    border-bottom: 1px solid var(--divider);
}

/* Optimized column widths */
.device-header, .device-cell {
    width: 120px;  /* Slightly narrower */
}

.entity-header, .entity-cell {
    width: auto;  /* Takes remaining space */
    min-width: 150px;  /* But don't go too narrow */
    max-width: 300px;  /* And don't get too wide */
}

.checkbox-header, .checkbox-cell {
    width: 60px;  /* Slightly narrower */
    text-align: center;
}

td {
    padding: 8px 4px;  /* Reduced horizontal padding */
    border-bottom: 1px solid var(--divider);
}

/* Tooltip styling - all elements with title attribute */
[title] {
    cursor: help;
    position: relative;
}

/* Visual indicator for hoverable items */
.device-name, .entity-friendly {
    border-bottom: 1px dotted var(--text-secondary);
    display: inline-block;
    max-width: 100%;
}

/* Device column styling */
.device-name {
    font-size: 12px;
    color: var(--primary-color);
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    padding-right: 4px;
}

/* Entity display - more compact */
.entity-name {
    display: block;
    width: 100%;
}

.entity-friendly {
    font-weight: 500;
    font-size: 13px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    width: 100%;
    padding-right: 4px;
}

.entity-friendly:hover {
    border-bottom-color: var(--text-secondary);
}

/* No need for entity-id since it's in tooltip */

/* Checkbox column */
.checkbox-cell {
    text-align: center;
    padding-left: 2px;
    padding-right: 2px;
}

.entity-checkbox {
    width: 16px;
    height: 16px;
    cursor: pointer;
    margin: 0;
}

/* Compact action bar */
.action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    flex-wrap: wrap;
    gap: 8px;
}

.select-all {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
}

.select-all input[type="checkbox"] {
    width: 16px;
    height: 16px;
    margin: 0;
}

.save-btn {
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 20px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: opacity 0.2s;
}

.save-btn:hover {
    opacity: 0.8;
}

.save-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 30px 20px;
}

.empty-message {
    max-width: 300px;
    margin: 0 auto;
}

.empty-icon {
    font-size: 40px;
    display: block;
    margin-bottom: 10px;
    opacity: 0.5;
}

.empty-message h3 {
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 5px;
}

.empty-message p {
    color: var(--text-secondary);
    font-size: 13px;
    line-height: 1.4;
}

/* Compact config guide */
.config-steps {
    padding-left: 16px;
    margin: 8px 0;
    font-size: 13px;
}

.config-steps li {
    margin-bottom: 4px;
    color: var(--text-secondary);
}

.note {
    color: var(--text-secondary);
    font-style: italic;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--divider);
    font-size: 12px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    body {
        padding: 8px;
    }
    
    .filter-bar {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .filter-bar select {
        width: 100%;
    }
    
    .stats {
        margin-left: 0;
    }
    
    .setting-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }
    
    .action-bar {
        flex-direction: column;
        align-items: stretch;
    }
    
    .save-btn {
        width: 100%;
    }
    
    /* On mobile, remove fixed widths */
    table {
        table-layout: auto;
    }
    
    .device-header, .device-cell,
    .entity-header, .entity-cell,
    .checkbox-header, .checkbox-cell {
        width: auto;
    }
}

/* For very large screens, entity column can be wider */
@media (min-width: 1200px) {
    .entity-header, .entity-cell {
        max-width: 400px;
    }
}
"""