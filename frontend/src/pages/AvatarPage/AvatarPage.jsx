import React, { useState, useEffect } from 'react';
import './AvatarPage.css';
import { getMommyData, equipAccessory, unequipAccessory } from '../../services/mommyService';

const AvatarPage = () => {
    const [mommyData, setMommyData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState('hair');

    useEffect(() => {
        fetchMommyData();
    }, []);

    const fetchMommyData = async () => {
        try {
            const data = await getMommyData();
            setMommyData(data);
        } catch (error) {
            console.error('Error fetching mommy data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleEquip = async (accessoryName, slot) => {
        try {
            const result = await equipAccessory(accessoryName, slot);
            if (result.success) {
                setMommyData(result.mommy);
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error('Error equipping accessory:', error);
            alert('Failed to equip accessory');
        }
    };

    const handleUnequip = async (slot) => {
        try {
            const result = await unequipAccessory(slot);
            if (result.success) {
                setMommyData(result.mommy);
            }
        } catch (error) {
            console.error('Error unequipping accessory:', error);
        }
    };

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    const categories = ['hair', 'hat', 'shirt', 'pants', 'shoes'];
    const ownedByCategory = mommyData?.owned_accessories.reduce((acc, item) => {
        if (!acc[item.category]) acc[item.category] = [];
        acc[item.category].push(item);
        return acc;
    }, {}) || {};

    return (
        <div className="avatar-page">
            <div className="avatar-header">
                <h1>💯 Dress Your Avatar</h1>
                <p>Click items to dress up!</p>
            </div>

            <div className="avatar-content">
                {/* Character Display */}
                <div className="character-section">
                    <div className="character-canvas">
                        {/* Base */}
                        <img 
                            src="/assets/customizables/base/mommy_base.png" 
                            alt="Base"
                            className="character-layer base-layer"
                        />
                        
                        {/* Hair Back */}
                        {mommyData?.equipped?.hair?.back && (
                            <img 
                                src={mommyData.equipped.hair.back} 
                                alt="Hair Back"
                                className="character-layer hair-back-layer"
                            />
                        )}
                        
                        {/* Pants */}
                        {mommyData?.equipped?.pants?.front && (
                            <img 
                                src={mommyData.equipped.pants.front} 
                                alt="Pants"
                                className="character-layer pants-layer"
                            />
                        )}
                        
                        {/* Shirt */}
                        {mommyData?.equipped?.shirt?.front && (
                            <img 
                                src={mommyData.equipped.shirt.front} 
                                alt="Shirt"
                                className="character-layer shirt-layer"
                            />
                        )}
                        
                        {/* Shoes */}
                        {mommyData?.equipped?.shoes?.front && (
                            <img 
                                src={mommyData.equipped.shoes.front} 
                                alt="Shoes"
                                className="character-layer shoes-layer"
                            />
                        )}
                        
                        {/* Hair Front */}
                        {mommyData?.equipped?.hair?.front && (
                            <img 
                                src={mommyData.equipped.hair.front} 
                                alt="Hair"
                                className="character-layer hair-front-layer"
                            />
                        )}
                        
                        {/* Hat */}
                        {mommyData?.equipped?.hat?.front && (
                            <img 
                                src={mommyData.equipped.hat.front} 
                                alt="Hat"
                                className="character-layer hat-layer"
                            />
                        )}
                    </div>

                    {/* Currently Equipped Info */}
                    <div className="equipped-info">
                        <h3>Currently Equipped</h3>
                        {categories.map(slot => (
                            <div key={slot} className="equipped-item">
                                <span className="slot-name">{slot}:</span>
                                <span className="slot-value">
                                    {mommyData?.equipped?.[slot]?.name || 'None'}
                                </span>
                                {mommyData?.equipped?.[slot] && (
                                    <button 
                                        className="unequip-btn"
                                        onClick={() => handleUnequip(slot)}
                                    >
                                        ✕
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Accessory Selection */}
                <div className="accessories-section">
                    <div className="category-tabs">
                        {categories.map(cat => (
                            <button
                                key={cat}
                                className={`category-tab ${selectedCategory === cat ? 'active' : ''}`}
                                onClick={() => setSelectedCategory(cat)}
                            >
                                {cat.charAt(0).toUpperCase() + cat.slice(1)}
                            </button>
                        ))}
                    </div>

                    <div className="accessories-grid">
                        {ownedByCategory[selectedCategory]?.length > 0 ? (
                            ownedByCategory[selectedCategory].map((accessory, index) => (
                                <div 
                                    key={index}
                                    className={`accessory-item ${
                                        mommyData?.equipped?.[selectedCategory]?.name === accessory.name 
                                            ? 'selected' 
                                            : ''
                                    }`}
                                    onClick={() => handleEquip(accessory.name, selectedCategory)}
                                >
                                    <div className="accessory-preview">
                                        <img 
                                            src={accessory.front} 
                                            alt={accessory.name}
                                        />
                                    </div>
                                    <div className="accessory-name">{accessory.name}</div>
                                    {mommyData?.equipped?.[selectedCategory]?.name === accessory.name && (
                                        <div className="equipped-badge">✓</div>
                                    )}
                                </div>
                            ))
                        ) : (
                            <div className="no-accessories">
                                <p>No {selectedCategory} items owned</p>
                                <p className="hint">Visit the shop to buy items!</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AvatarPage;