// Beauty Parlour Inventory Management Database
class InventoryDatabase {
    constructor() {
        this.dbName = 'BeautyParlourDB';
        this.dbVersion = 1;
        this.db = null;
    }

    // Initialize the database
    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);

            request.onerror = (event) => {
                console.error('Database error:', event.target.error);
                reject(event.target.error);
            };

            request.onsuccess = (event) => {
                this.db = event.target.result;
                console.log('Database initialized successfully');
                resolve(this.db);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                // Create inventory table
                if (!db.objectStoreNames.contains('inventory')) {
                    const inventoryStore = db.createObjectStore('inventory', { 
                        keyPath: 'id', 
                        autoIncrement: true 
                    });
                    
                    // Create indexes for searching
                    inventoryStore.createIndex('name', 'name', { unique: false });
                    inventoryStore.createIndex('category', 'category', { unique: false });
                    inventoryStore.createIndex('sku', 'sku', { unique: true });
                    inventoryStore.createIndex('low_stock', 'quantity', { unique: false });
                }

                // Create categories table
                if (!db.objectStoreNames.contains('categories')) {
                    const categoryStore = db.createObjectStore('categories', { 
                        keyPath: 'id', 
                        autoIncrement: true 
                    });
                    categoryStore.createIndex('name', 'name', { unique: true });
                }

                // Create suppliers table
                if (!db.objectStoreNames.contains('suppliers')) {
                    const supplierStore = db.createObjectStore('suppliers', { 
                        keyPath: 'id', 
                        autoIncrement: true 
                    });
                    supplierStore.createIndex('name', 'name', { unique: false });
                }

                // Create transactions table
                if (!db.objectStoreNames.contains('transactions')) {
                    const transactionStore = db.createObjectStore('transactions', { 
                        keyPath: 'id', 
                        autoIncrement: true 
                    });
                    transactionStore.createIndex('date', 'date', { unique: false });
                    transactionStore.createIndex('type', 'type', { unique: false });
                    transactionStore.createIndex('item_id', 'item_id', { unique: false });
                }
            };
        });
    }

    // Add new inventory item
    async addInventoryItem(item) {
        const transaction = this.db.transaction(['inventory'], 'readwrite');
        const store = transaction.objectStore('inventory');
        
        // Add timestamps
        item.created_at = new Date().toISOString();
        item.updated_at = new Date().toISOString();
        
        return new Promise((resolve, reject) => {
            const request = store.add(item);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Get all inventory items
    async getAllInventoryItems() {
        const transaction = this.db.transaction(['inventory'], 'readonly');
        const store = transaction.objectStore('inventory');
        
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Get inventory item by ID
    async getInventoryItem(id) {
        const transaction = this.db.transaction(['inventory'], 'readonly');
        const store = transaction.objectStore('inventory');
        
        return new Promise((resolve, reject) => {
            const request = store.get(id);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Update inventory item
    async updateInventoryItem(item) {
        const transaction = this.db.transaction(['inventory'], 'readwrite');
        const store = transaction.objectStore('inventory');
        
        // Update timestamp
        item.updated_at = new Date().toISOString();
        
        return new Promise((resolve, reject) => {
            const request = store.put(item);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Delete inventory item
    async deleteInventoryItem(id) {
        const transaction = this.db.transaction(['inventory'], 'readwrite');
        const store = transaction.objectStore('inventory');
        
        return new Promise((resolve, reject) => {
            const request = store.delete(id);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Search inventory items
    async searchInventoryItems(searchTerm, category = null) {
        const transaction = this.db.transaction(['inventory'], 'readonly');
        const store = transaction.objectStore('inventory');
        
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => {
                let items = request.result;
                
                // Filter by search term
                if (searchTerm) {
                    items = items.filter(item => 
                        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        item.sku.toLowerCase().includes(searchTerm.toLowerCase())
                    );
                }
                
                // Filter by category
                if (category) {
                    items = items.filter(item => item.category === category);
                }
                
                resolve(items);
            };
            request.onerror = () => reject(request.error);
        });
    }

    // Get low stock items
    async getLowStockItems(threshold = 10) {
        const transaction = this.db.transaction(['inventory'], 'readonly');
        const store = transaction.objectStore('inventory');
        
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => {
                const items = request.result.filter(item => item.quantity <= threshold);
                resolve(items);
            };
            request.onerror = () => reject(request.error);
        });
    }

    // Add category
    async addCategory(category) {
        const transaction = this.db.transaction(['categories'], 'readwrite');
        const store = transaction.objectStore('categories');
        
        return new Promise((resolve, reject) => {
            const request = store.add(category);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Get all categories
    async getAllCategories() {
        const transaction = this.db.transaction(['categories'], 'readonly');
        const store = transaction.objectStore('categories');
        
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Record transaction
    async addTransaction(transaction) {
        const tx = this.db.transaction(['transactions'], 'readwrite');
        const store = tx.objectStore('transactions');
        
        transaction.date = new Date().toISOString();
        
        return new Promise((resolve, reject) => {
            const request = store.add(transaction);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Update stock quantity
    async updateStock(itemId, newQuantity, transactionType = 'adjustment') {
        const transaction = this.db.transaction(['inventory', 'transactions'], 'readwrite');
        const inventoryStore = transaction.objectStore('inventory');
        const transactionStore = transaction.objectStore('transactions');
        
        return new Promise((resolve, reject) => {
            // Get current item
            const getRequest = inventoryStore.get(itemId);
            getRequest.onsuccess = () => {
                const item = getRequest.result;
                const oldQuantity = item.quantity;
                item.quantity = newQuantity;
                item.updated_at = new Date().toISOString();
                
                // Update item
                const updateRequest = inventoryStore.put(item);
                updateRequest.onsuccess = () => {
                    // Record transaction
                    const transactionRecord = {
                        item_id: itemId,
                        item_name: item.name,
                        type: transactionType,
                        old_quantity: oldQuantity,
                        new_quantity: newQuantity,
                        difference: newQuantity - oldQuantity,
                        date: new Date().toISOString()
                    };
                    
                    const transRequest = transactionStore.add(transactionRecord);
                    transRequest.onsuccess = () => resolve(transactionRecord);
                    transRequest.onerror = () => reject(transRequest.error);
                };
                updateRequest.onerror = () => reject(updateRequest.error);
            };
            getRequest.onerror = () => reject(getRequest.error);
        });
    }
}

// Initialize database instance
const inventoryDB = new InventoryDatabase();
