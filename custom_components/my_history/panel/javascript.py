"""JavaScript code for My History panel - HTTP only version."""
JAVASCRIPT_CODE = """
// Save selections using HTTP POST
async function saveSelections() {
    const saveBtn = document.querySelector('.save-btn');
    const originalText = saveBtn.textContent;
    saveBtn.textContent = 'Saving...';
    saveBtn.disabled = true;
    
    try {
        const selected = collectSelectedEntities();
        const purgeDays = getPurgeDays();
        
        console.log(`Saving ${selected.length} entities, purge days: ${purgeDays}`);
        
        const response = await fetch('/api/my_history/selections', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tracked_entities: selected,
                purge_keep_days: purgeDays
            })
        });
        
        if (response.ok) {
            alert('✓ Selections saved successfully!\\n\\nRestart Home Assistant to apply changes.');
        } else {
            const error = await response.text();
            throw new Error(`HTTP ${response.status}: ${error}`);
        }
        
    } catch (error) {
        console.error('Save error:', error);
        alert('❌ Error saving selections: ' + error.message);
    } finally {
        saveBtn.textContent = originalText;
        saveBtn.disabled = false;
    }
}

// Collect selected entities
function collectSelectedEntities() {
    const selected = [];
    document.querySelectorAll('.entity-checkbox').forEach(cb => {
        if (cb.checked) selected.push(cb.dataset.entityId);
    });
    return selected;
}

// Get purge days value
function getPurgeDays() {
    const input = document.getElementById('purge-days');
    const value = input ? parseInt(input.value) : 30;
    return isNaN(value) ? 30 : Math.min(365, Math.max(1, value));
}

// Device filtering
function filterByDevice(deviceId) {
    const rows = document.querySelectorAll('tbody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        if (!deviceId || row.dataset.deviceId === deviceId) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    const stats = document.getElementById('visible-count');
    const total = rows.length;
    
    if (stats) {
        if (visibleCount === 0) {
            stats.textContent = 'No entities match filter';
        } else if (visibleCount === total) {
            stats.textContent = 'Showing all entities';
        } else {
            stats.textContent = `Showing ${visibleCount} of ${total} entities`;
        }
    }
    
    updateSelectAllState();
}

// Select all visible checkboxes
function toggleAll(source) {
    document.querySelectorAll('tbody tr:not([style*="display: none"]) .entity-checkbox')
        .forEach(cb => cb.checked = source.checked);
    updateSelectAllState();
}

// Update select all checkbox state
function updateSelectAllState() {
    const visible = document.querySelectorAll('tbody tr:not([style*="display: none"]) .entity-checkbox');
    const checked = document.querySelectorAll('tbody tr:not([style*="display: none"]) .entity-checkbox:checked');
    const selectAll = document.getElementById('select-all');
    
    if (!selectAll) return;
    
    if (visible.length === 0) {
        selectAll.checked = false;
        selectAll.indeterminate = false;
        selectAll.disabled = true;
    } else {
        selectAll.disabled = false;
        selectAll.checked = checked.length === visible.length;
        selectAll.indeterminate = checked.length > 0 && checked.length < visible.length;
    }
}

// Update select all state when individual checkboxes change
document.addEventListener('change', function(e) {
    if (e.target.classList.contains('entity-checkbox')) {
        updateSelectAllState();
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('My History panel initializing...');
    filterByDevice('');
});
"""