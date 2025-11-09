import React, { useState, useEffect } from 'react';
import './ShopPage.css';
import { useUser } from '../../Hooks/userContext';
import { getShopData, buyAccessory } from '../../services/shopService';

const ShopPage = () => {
  const { user, updateBalance } = useUser();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Category mapping from display name to backend category
  const categoryMap = {
    'all': 'all',
    'hair': 'hair',
    'hat': 'hat',
    'shirt': 'shirt',
    'pants': 'pants',
    'shoes': 'shoes'
  };

  // Fetch products on component mount
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const data = await getShopData();
        setProducts(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching shop data:', err);
        setError('Failed to load products. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  // Filter products based on selected category
  const filteredProducts = selectedCategory === 'all' 
    ? products 
    : products.filter(product => product.category === selectedCategory);

  // Handle category filter click
  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
  };

  // Handle buy button click
  const handleBuyProduct = async (productId) => {
    try {
      const result = await buyAccessory(productId);
      
      if (result.success) {
        // Update balance in context
        updateBalance(result.new_balance);
        
        // Remove product from local state
        setProducts(products.filter(p => p.id !== productId));
        
        // Optional: show success message
        alert(result.message);
      } else {
        alert(result.message);
      }
    } catch (err) {
      console.error('Error buying product:', err);
      alert('Failed to purchase item. Please try again.');
    }
  };

  // Show loading state
  if (loading) {
    return (
      <div className="shop-container">
        <div className="shop-header">
          <h1 className="shop-title">🏪 Accessory Shop</h1>
          <p className="shop-subtitle">Loading products...</p>
        </div>
        <div className="loading-spinner">⏳ Loading...</div>
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="shop-container">
        <div className="shop-header">
          <h1 className="shop-title">🏪 Accessory Shop</h1>
          <p className="shop-subtitle" style={{ color: '#ff6b6b' }}>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="shop-container">
      {/* Header Section */}
      <div className="shop-header">
        <h1 className="shop-title">🏪 Accessory Shop</h1>
        <p className="shop-subtitle">Everything you need for your little one!</p>
        <div className="shop-balance">
          <span className="balance-label">Your Balance:</span>
          <span className="balance-amount">💰 ${user?.balance.toFixed(2)}</span>
        </div>
      </div>

      {/* Filter Buttons */}
      <div className="shop-filters">
        <button 
          className={`filter-btn ${selectedCategory === 'all' ? 'filter-active' : ''}`}
          onClick={() => handleCategoryClick('all')}
        >
          All Items
        </button>
        <button 
          className={`filter-btn ${selectedCategory === 'hair' ? 'filter-active' : ''}`}
          onClick={() => handleCategoryClick('hair')}
        >
          Hairstyles
        </button>
        <button 
          className={`filter-btn ${selectedCategory === 'hat' ? 'filter-active' : ''}`}
          onClick={() => handleCategoryClick('hat')}
        >
          Hats
        </button>
        <button 
          className={`filter-btn ${selectedCategory === 'shirt' ? 'filter-active' : ''}`}
          onClick={() => handleCategoryClick('shirt')}
        >
          Tops
        </button>
        <button 
          className={`filter-btn ${selectedCategory === 'pants' ? 'filter-active' : ''}`}
          onClick={() => handleCategoryClick('pants')}
        >
          Bottoms
        </button>
        <button 
          className={`filter-btn ${selectedCategory === 'shoes' ? 'filter-active' : ''}`}
          onClick={() => handleCategoryClick('shoes')}
        >
          Shoes
        </button>
      </div>

      {/* Products Grid */}
      <div className="products-grid">
        {filteredProducts.length === 0 ? (
          <div className="no-products">
            <p>No {selectedCategory === 'all' ? 'products' : selectedCategory} items available at the moment.</p>
          </div>
        ) : (
          filteredProducts.map((product) => (
            <div key={product.id} className="product-card">
              <div className="product-back_image">
                <img src={product.image} alt={product.name} width="200" height="200"/>
              </div>

              <div className="product-category">{product.category}</div>
              <h3 className="product-name">{product.name}</h3>
              <div className="product-price">${product.price}</div>
              <button 
                className="buy-button"
                onClick={() => handleBuyProduct(product.id)}
              >
                <span className="button-icon">🛒</span>
                <span className="button-text">Buy Now</span>
              </button>
            </div>
          ))
        )}
      </div>

    </div>
  );
};

export default ShopPage;