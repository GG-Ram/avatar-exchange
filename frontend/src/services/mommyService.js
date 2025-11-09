import { get, post } from '../util/util';

// Helper function to adapt accessory data from backend format to frontend format
const adaptAccessory = (accessory) => {
    if (!accessory) return null;
    
    console.log('🔧 adaptAccessory - Before:', accessory);
    
    const adapted = {
        ...accessory,
        front: accessory.frontimg || accessory.image,  // Use frontimg, fallback to image
        back: accessory.backimg || null                 // Use backimg
    };
    
    console.log('🔧 adaptAccessory - After:', adapted);
    return adapted;
};

// Helper function to adapt mommy data
const adaptMommyData = (data) => {
    if (!data) return null;
    
    console.log('📦 adaptMommyData - Raw data:', data);
    console.log('📦 Owned accessories count:', data.owned_accessories?.length);
    console.log('📦 Equipped slots:', Object.keys(data.equipped || {}));
    
    const adapted = {
        ...data,
        owned_accessories: data.owned_accessories?.map(adaptAccessory) || [],
        equipped: data.equipped ? Object.keys(data.equipped).reduce((acc, slot) => {
            console.log(`📦 Processing equipped slot [${slot}]:`, data.equipped[slot]);
            acc[slot] = adaptAccessory(data.equipped[slot]);
            return acc;
        }, {}) : {}
    };
    
    console.log('📦 adaptMommyData - Final adapted data:', adapted);
    return adapted;
};

export const getMommyData = async () => {
    console.log('🎯 getMommyData - Fetching...');
    const data = await get('/mommy');
    console.log('🎯 getMommyData - Raw response:', data);
    const adapted = adaptMommyData(data);
    console.log('🎯 getMommyData - Returning:', adapted);
    return adapted;
}

export const equipAccessory = async (accessoryName, slot) => {
    console.log(`⚡ equipAccessory - Equipping ${accessoryName} to ${slot}`);
    const result = await post('/mommy/equip', { 
        accessory_name: accessoryName, 
        slot: slot 
    });
    
    console.log('⚡ equipAccessory - Raw result:', result);
    
    if (result.mommy) {
        result.mommy = adaptMommyData(result.mommy);
    }
    
    console.log('⚡ equipAccessory - Final result:', result);
    return result;
}

export const unequipAccessory = async (slot) => {
    console.log(`🔓 unequipAccessory - Unequipping ${slot}`);
    const result = await post('/mommy/unequip', { slot: slot });
    
    console.log('🔓 unequipAccessory - Raw result:', result);
    
    if (result.mommy) {
        result.mommy = adaptMommyData(result.mommy);
    }
    
    console.log('🔓 unequipAccessory - Final result:', result);
    return result;
}

export const getOwnedAccessories = async () => {
    console.log('🛍️ getOwnedAccessories - Fetching...');
    const data = await get('/mommy/owned');
    
    console.log('🛍️ getOwnedAccessories - Raw data:', data);
    
    if (data.owned_accessories) {
        data.owned_accessories = data.owned_accessories.map(adaptAccessory);
    }
    
    console.log('🛍️ getOwnedAccessories - Final data:', data);
    return data;
}

export const addAccessoryToMommy = async (accessoryName) => {
    console.log(`➕ addAccessoryToMommy - Adding ${accessoryName}`);
    const result = await post('/mommy/addAccessory', { 
        accessory_name: accessoryName 
    });
    
    console.log('➕ addAccessoryToMommy - Raw result:', result);
    
    if (result.mommy) {
        result.mommy = adaptMommyData(result.mommy);
    }
    
    console.log('➕ addAccessoryToMommy - Final result:', result);
    return result;
}