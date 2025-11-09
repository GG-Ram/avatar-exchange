import { get, post } from '../util/util';

export const getMommyData = async () => {
    return await get('/mommy');
}

export const equipAccessory = async (accessoryName, slot) => {
    return await post('/mommy/equip', { 
        accessory_name: accessoryName, 
        slot: slot 
    });
}

export const unequipAccessory = async (slot) => {
    return await post('/mommy/unequip', { slot: slot });
}

export const getOwnedAccessories = async () => {
    return await get('/mommy/owned');
}

export const addAccessoryToMommy = async (accessoryName) => {
    return await post('/mommy/addAccessory', { 
        accessory_name: accessoryName 
    });
}