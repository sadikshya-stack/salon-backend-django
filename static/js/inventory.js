// Inventory Management JavaScript
class InventoryManager {
    constructor() {
        this.db = null;
        this.currentItems = [];
        this.init();
    }

    async init() {
        try {
            // Initialize database
            this.db = await inventoryDB.init();
            
            // Load initial data
            await this.loadInventoryItems();
            await this.updateStatistics();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Add sample data if database is empty
            await this.addSampleDataIfNeeded();
            
        } catch (error) {
            console.error('Failed to initialize inventory:', error);
            this.showNotification('Failed to initialize inventory system', 'error');
        }
    }

    setupEventListeners() {
        // Add item form
        document.getElementById('saveItemBtn').addEventListener('click', () => this.saveNewItem());
        
        // Edit item form
        document.getElementById('updateItemBtn').addEventListener('click', () => this.updateItem());
        
        // Search and filters
        document.getElementById('searchInput').addEventListener('input', () => this.filterItems());
        document.getElementById('categoryFilter').addEventListener('change', () => this.filterItems());
        document.getElementById('stockFilter').addEventListener('change', () => this.filterItems());
        
        // Form validation
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => e.preventDefault());
        });
    }

    async loadInventoryItems() {
        try {
            this.currentItems = await this.db.getAllInventoryItems();
            this.renderInventoryTable(this.currentItems);
        } catch (error) {
            console.error('Failed to load inventory items:', error);
        }
    }

    renderInventoryTable(items) {
        const tbody = document.getElementById('inventoryTableBody');
        const emptyState = document.getElementById('emptyState');
        
        if (items.length === 0) {
            tbody.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }
        
        emptyState.style.display = 'none';
        tbody.innerHTML = items.map(item => this.createInventoryRow(item)).join('');
    }

    createInventoryRow(item) {
        const stockStatus = this.getStockStatus(item.quantity, item.reorder_level || 10);
        const totalValue = (item.quantity * item.price).toFixed(2);
        
        return `
            <tr class="${stockStatus.class}">
                <td>${item.sku}</td>
                <td>
                    <strong>${item.name}</strong>
                    ${item.description ? `<br><small class="text-muted">${item.description.substring(0, 50)}...</small>` : ''}
                </td>
                <td><span class="category-badge">${this.formatCategory(item.category)}</span></td>
                <td>
                    <span class="stock-indicator ${stockStatus.indicator}"></span>
                    ${item.quantity}
                </td>
                <td>$${item.price.toFixed(2)}</td>
                <td>$${totalValue}</td>
                <td>${stockStatus.label}</td>
                <td class="action-buttons">
                    <button class="btn btn-sm btn-outline-primary" onclick="inventoryManager.editItem(${item.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-success" onclick="inventoryManager.adjustStock(${item.id})">
                        <i class="fas fa-plus-minus"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="inventoryManager.deleteItem(${item.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }

    getStockStatus(quantity, reorderLevel) {
        if (quantity === 0) {
            return { 
                label: 'Out of Stock', 
                class: 'out-of-stock', 
                indicator: 'stock-out' 
            };
        } else if (quantity <= reorderLevel) {
            return { 
                label: 'Low Stock', 
                class: 'low-stock', 
                indicator: 'stock-low' 
            };
        } else if (quantity <= reorderLevel * 2) {
            return { 
                label: 'Medium Stock', 
                class: '', 
                indicator: 'stock-medium' 
            };
        } else {
            return { 
                label: 'In Stock', 
                class: '', 
                indicator: 'stock-high' 
            };
        }
    }

    formatCategory(category) {
        const categories = {
            'hair-care': 'Hair Care',
            'skincare': 'Skincare',
            'makeup': 'Makeup',
            'nail-care': 'Nail Care',
            'tools': 'Tools & Equipment',
            'cleaning': 'Cleaning Supplies'
        };
        return categories[category] || category;
    }

    async saveNewItem() {
        try {
            const form = document.getElementById('addItemForm');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            const item = {
                sku: document.getElementById('itemSku').value,
                name: document.getElementById('itemName').value,
                category: document.getElementById('itemCategory').value,
                supplier: document.getElementById('itemSupplier').value,
                quantity: parseInt(document.getElementById('itemQuantity').value),
                price: parseFloat(document.getElementById('itemPrice').value),
                reorder_level: parseInt(document.getElementById('itemReorderLevel').value) || 10,
                description: document.getElementById('itemDescription').value
            };

            await this.db.addInventoryItem(item);
            await this.loadInventoryItems();
            await this.updateStatistics();
            
            // Close modal and reset form
            const modal = bootstrap.Modal.getInstance(document.getElementById('addItemModal'));
            modal.hide();
            form.reset();
            
            this.showNotification('Item added successfully', 'success');
        } catch (error) {
            console.error('Failed to add item:', error);
            this.showNotification('Failed to add item', 'error');
        }
    }

    async editItem(id) {
        try {
            const item = await this.db.getInventoryItem(id);
            if (!item) return;

            // Populate edit form
            document.getElementById('editItemId').value = item.id;
            document.getElementById('editItemSku').value = item.sku;
            document.getElementById('editItemName').value = item.name;
            document.getElementById('editItemCategory').value = item.category;
            document.getElementById('editItemSupplier').value = item.supplier || '';
            document.getElementById('editItemQuantity').value = item.quantity;
            document.getElementById('editItemPrice').value = item.price;
            document.getElementById('editItemReorderLevel').value = item.reorder_level || 10;
            document.getElementById('editItemDescription').value = item.description || '';

            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('editItemModal'));
            modal.show();
        } catch (error) {
            console.error('Failed to load item for editing:', error);
            this.showNotification('Failed to load item', 'error');
        }
    }

    async updateItem() {
        try {
            const form = document.getElementById('editItemForm');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            const item = {
                id: parseInt(document.getElementById('editItemId').value),
                sku: document.getElementById('editItemSku').value,
                name: document.getElementById('editItemName').value,
                category: document.getElementById('editItemCategory').value,
                supplier: document.getElementById('editItemSupplier').value,
                quantity: parseInt(document.getElementById('editItemQuantity').value),
                price: parseFloat(document.getElementById('editItemPrice').value),
                reorder_level: parseInt(document.getElementById('editItemReorderLevel').value) || 10,
                description: document.getElementById('editItemDescription').value
            };

            await this.db.updateInventoryItem(item);
            await this.loadInventoryItems();
            await this.updateStatistics();
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('editItemModal'));
            modal.hide();
            
            this.showNotification('Item updated successfully', 'success');
        } catch (error) {
            console.error('Failed to update item:', error);
            this.showNotification('Failed to update item', 'error');
        }
    }

    async deleteItem(id) {
        if (!confirm('Are you sure you want to delete this item?')) return;

        try {
            await this.db.deleteInventoryItem(id);
            await this.loadInventoryItems();
            await this.updateStatistics();
            
            this.showNotification('Item deleted successfully', 'success');
        } catch (error) {
            console.error('Failed to delete item:', error);
            this.showNotification('Failed to delete item', 'error');
        }
    }

    async adjustStock(id) {
        try {
            const item = await this.db.getInventoryItem(id);
            if (!item) return;

            const newQuantity = prompt(`Adjust stock for "${item.name}"\nCurrent quantity: ${item.quantity}\nEnter new quantity:`, item.quantity);
            
            if (newQuantity === null) return;
            
            const quantity = parseInt(newQuantity);
            if (isNaN(quantity) || quantity < 0) {
                this.showNotification('Invalid quantity', 'error');
                return;
            }

            await this.db.updateStock(id, quantity, 'manual_adjustment');
            await this.loadInventoryItems();
            await this.updateStatistics();
            
            this.showNotification('Stock adjusted successfully', 'success');
        } catch (error) {
            console.error('Failed to adjust stock:', error);
            this.showNotification('Failed to adjust stock', 'error');
        }
    }

    filterItems() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const categoryFilter = document.getElementById('categoryFilter').value;
        const stockFilter = document.getElementById('stockFilter').value;

        let filteredItems = this.currentItems;

        // Search filter
        if (searchTerm) {
            filteredItems = filteredItems.filter(item => 
                item.name.toLowerCase().includes(searchTerm) ||
                item.sku.toLowerCase().includes(searchTerm) ||
                (item.description && item.description.toLowerCase().includes(searchTerm))
            );
        }

        // Category filter
        if (categoryFilter) {
            filteredItems = filteredItems.filter(item => item.category === categoryFilter);
        }

        // Stock filter
        if (stockFilter) {
            filteredItems = filteredItems.filter(item => {
                const status = this.getStockStatus(item.quantity, item.reorder_level || 10);
                switch (stockFilter) {
                    case 'in-stock':
                        return status.label === 'In Stock' || status.label === 'Medium Stock';
                    case 'low-stock':
                        return status.label === 'Low Stock';
                    case 'out-of-stock':
                        return status.label === 'Out of Stock';
                    default:
                        return true;
                }
            });
        }

        this.renderInventoryTable(filteredItems);
    }

    async updateStatistics() {
        try {
            const items = this.currentItems;
            
            // Total items
            document.getElementById('totalItems').textContent = items.length;
            
            // Low stock items
            const lowStockItems = items.filter(item => {
                const status = this.getStockStatus(item.quantity, item.reorder_level || 10);
                return status.label === 'Low Stock';
            });
            document.getElementById('lowStockItems').textContent = lowStockItems.length;
            
            // Out of stock items
            const outOfStockItems = items.filter(item => item.quantity === 0);
            document.getElementById('outOfStockItems').textContent = outOfStockItems.length;
            
            // Total value
            const totalValue = items.reduce((sum, item) => sum + (item.quantity * item.price), 0);
            document.getElementById('totalValue').textContent = `$${totalValue.toFixed(2)}`;
            
        } catch (error) {
            console.error('Failed to update statistics:', error);
        }
    }

    async addSampleDataIfNeeded() {
        try {
            const items = await this.db.getAllInventoryItems();
            
            // Always add all beauty parlour items
            const sampleItems = [
                    {
                        sku: 'HC001',
                        name: 'Professional Shampoo',
                        category: 'hair-care',
                        supplier: 'Beauty Supply Co.',
                        quantity: 25,
                        price: 15.99,
                        reorder_level: 10,
                        description: 'Professional grade shampoo for all hair types'
                    },
                    {
                        sku: 'SK001',
                        name: 'Face Cleanser',
                        category: 'skincare',
                        supplier: 'Skincare Pro',
                        quantity: 8,
                        price: 22.50,
                        reorder_level: 10,
                        description: 'Gentle facial cleanser for daily use'
                    },
                    {
                        sku: 'MK001',
                        name: 'Foundation - Natural',
                        category: 'makeup',
                        supplier: 'Makeup Pro',
                        quantity: 15,
                        price: 18.75,
                        reorder_level: 8,
                        description: 'Liquid foundation with SPF 15'
                    },
                    {
                        sku: 'NC001',
                        name: 'Nail Polish Red',
                        category: 'nail-care',
                        supplier: 'Nail Supplies',
                        quantity: 0,
                        price: 8.99,
                        reorder_level: 5,
                        description: 'Classic red nail polish'
                    },
                    {
                        sku: 'TL001',
                        name: 'Hair Cutting Scissors',
                        category: 'tools',
                        supplier: 'Pro Tools',
                        quantity: 5,
                        price: 45.00,
                        reorder_level: 2,
                        description: 'Professional hair cutting scissors'
                    },
                    {
                        sku: 'HC002',
                        name: 'Hair Conditioner',
                        category: 'hair-care',
                        supplier: 'Beauty Supply Co.',
                        quantity: 20,
                        price: 12.99,
                        reorder_level: 8,
                        description: 'Moisturizing conditioner for treated hair'
                    },
                    {
                        sku: 'HC003',
                        name: 'Hair Color - Black',
                        category: 'hair-care',
                        supplier: 'Color Pro',
                        quantity: 12,
                        price: 8.50,
                        reorder_level: 6,
                        description: 'Permanent hair color kit'
                    },
                    {
                        sku: 'HC004',
                        name: 'Hair Spray',
                        category: 'hair-care',
                        supplier: 'Beauty Supply Co.',
                        quantity: 18,
                        price: 6.99,
                        reorder_level: 10,
                        description: 'Extra hold hair spray'
                    },
                    {
                        sku: 'SK002',
                        name: 'Face Moisturizer',
                        category: 'skincare',
                        supplier: 'Skincare Pro',
                        quantity: 14,
                        price: 25.99,
                        reorder_level: 8,
                        description: 'Daily moisturizer with vitamin E'
                    },
                    {
                        sku: 'SK003',
                        name: 'Face Mask - Hydrating',
                        category: 'skincare',
                        supplier: 'Skincare Pro',
                        quantity: 25,
                        price: 4.99,
                        reorder_level: 15,
                        description: 'Single use hydrating face masks'
                    },
                    {
                        sku: 'MK002',
                        name: 'Lipstick - Red',
                        category: 'makeup',
                        supplier: 'Makeup Pro',
                        quantity: 20,
                        price: 12.50,
                        reorder_level: 10,
                        description: 'Classic red lipstick'
                    },
                    {
                        sku: 'MK003',
                        name: 'Mascara - Black',
                        category: 'makeup',
                        supplier: 'Makeup Pro',
                        quantity: 16,
                        price: 10.99,
                        reorder_level: 8,
                        description: 'Waterproof mascara'
                    },
                    {
                        sku: 'NC002',
                        name: 'Nail File',
                        category: 'nail-care',
                        supplier: 'Nail Supplies',
                        quantity: 30,
                        price: 2.99,
                        reorder_level: 20,
                        description: 'Emery nail files'
                    },
                    {
                        sku: 'NC003',
                        name: 'Cuticle Oil',
                        category: 'nail-care',
                        supplier: 'Nail Supplies',
                        quantity: 10,
                        price: 7.50,
                        reorder_level: 5,
                        description: 'Nourishing cuticle oil'
                    },
                    {
                        sku: 'TL002',
                        name: 'Hair Dryer',
                        category: 'tools',
                        supplier: 'Pro Tools',
                        quantity: 3,
                        price: 89.99,
                        reorder_level: 1,
                        description: 'Professional hair dryer'
                    },
                    {
                        sku: 'TL003',
                        name: 'Curling Iron',
                        category: 'tools',
                        supplier: 'Pro Tools',
                        quantity: 4,
                        price: 65.00,
                        reorder_level: 2,
                        description: '1 inch curling iron'
                    },
                    {
                        sku: 'CL001',
                        name: 'Disinfectant Spray',
                        category: 'cleaning',
                        supplier: 'Clean Supply',
                        quantity: 8,
                        price: 9.99,
                        reorder_level: 5,
                        description: 'Tool disinfectant spray'
                    },
                    {
                        sku: 'CL002',
                        name: 'Hand Sanitizer',
                        category: 'cleaning',
                        supplier: 'Clean Supply',
                        quantity: 15,
                        price: 3.99,
                        reorder_level: 10,
                        description: 'Hand sanitizer bottles'
                    },
                    {
                        sku: 'HC005',
                        name: 'Hair Gel',
                        category: 'hair-care',
                        supplier: 'Beauty Supply Co.',
                        quantity: 22,
                        price: 5.99,
                        reorder_level: 12,
                        description: 'Strong hold hair gel'
                    },
                    {
                        sku: 'SK004',
                        name: 'Sunscreen SPF 50',
                        category: 'skincare',
                        supplier: 'Skincare Pro',
                        quantity: 18,
                        price: 14.99,
                        reorder_level: 10,
                        description: 'Broad spectrum sunscreen'
                    }
                ];

                for (const item of sampleItems) {
                    // Always add the item (let it overwrite if exists)
                    try {
                        await this.db.addInventoryItem(item);
                    } catch (error) {
                        // If item exists, try to update it
                        try {
                            await this.db.updateInventoryItem(item.sku, item);
                        } catch (updateError) {
                            console.log('Could not add or update item:', item.sku);
                        }
                    }
                }

                await this.loadInventoryItems();
                await this.updateStatistics();
                
                // Force refresh the display
                setTimeout(() => {
                    this.loadInventoryItems();
                    this.updateStatistics();
                }, 1000);
                
                this.showNotification('Beauty parlour inventory items loaded', 'info');
        } catch (error) {
            console.error('Failed to add sample data:', error);
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Initialize inventory manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.inventoryManager = new InventoryManager();
});
