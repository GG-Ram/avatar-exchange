import React, { useState, useEffect } from 'react';
import './AvatarPage.css';
import { getMommyData, equipAccessory, unequipAccessory } from '../../services/mommyService';
import MommyAdvice from '../../components/MommyAdvice/MommyAdvice';

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
                        {/* ✅ Base Layer */}
                        <img 
                            src="https://media.discordapp.net/attachments/1436081196634341396/1437051372875939944/Untitled4_20251108134347.png?ex=6911d5e2&is=69108462&hm=9b95832ebe30a00b030102441d265db84d3b5e65dffdb502ce0ae6bb1d7bffec&=&format=webp&quality=lossless&width=1562&height=1562" 
                            alt="Base"
                            className="character-layer base-layer"
                        />

                        {/* ✅ Pants */}
                        {mommyData?.equipped?.pants && (
                            <img 
                                src={mommyData.equipped.pants.image}
                                alt="Pants"
                                className="character-layer pants-layer"
                            />
                        )}

                        {/* ✅ Shirt */}
                        {mommyData?.equipped?.shirt && (
                            <img 
                                src={mommyData.equipped.shirt.image}
                                alt="Shirt"
                                className="character-layer shirt-layer"
                            />
                        )}

                        {/* ✅ Shoes */}
                        {mommyData?.equipped?.shoes && (
                            <img 
                                src={mommyData.equipped.shoes.image}
                                alt="Shoes"
                                className="character-layer shoes-layer"
                            />
                        )}

                        {/* ✅ Hair */}
                        {mommyData?.equipped?.hair && (
                            <img 
                                src={mommyData.equipped.hair.image}
                                alt="Hair"
                                className="character-layer hair-layer"
                            />
                        )}

                        {/* ✅ Hat */}
                        {mommyData?.equipped?.hat && (
                            <img 
                                src={mommyData.equipped.hat.image}
                                alt="Hat"
                                className="character-layer hat-layer"
                            />
                        )}
                    </div>

                    {/* Equipped Info */}
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

                    {/* Financial Advice */}
                    <MommyAdvice />
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
                                            src={accessory.image}
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
