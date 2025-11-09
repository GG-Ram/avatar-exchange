class Accessory:
    def __init__(self, name, price, front_img=None, back_img=None):
        self.name = name
        self.price = price
        self.front = front_img
        self.back = back_img

hat1 = Accessory("Cowboy", 67.00, "/assets/customizables/hat/hat_1.png")
print(hat1.name)
hat2 = Accessory("Witch", 67.00, "/assets/customizables/hat/hat_2.png")
print(hat2.name)

hair1 = Accessory("Hair A", 67.00, "/assets/customizables/hair_top/hair_1t.png", "/assets/customizables/hair_bottom/hair_1b.png")
print(hair1.name)
hair2 = Accessory("Hair B", 67.00, "/assets/customizables/hair_top/hair_2t.png", "/assets/customizables/hair_bottom/hair_2b.png")
print(hair2.name)
hair3 = Accessory("Hair C", 67.00, "/assets/customizables/hair_top/hair_3t.png", "/assets/customizables/hair_bottom/hair_3b.png")
print(hair3.name)
hairDef = Accessory("Hair Default", 67.00, "/assets/customizables/hair_top/hair_t.png", "/assets/customizables/hair_bottom/hair_b.png")
print(hairDef.name)

pant1 = Accessory("Blue Jeans", 67.00, "/assets/customizables/pants/pants_1.png")
print(pant1.name)
pant2 = Accessory("Jean Shorts", 67.00, "/assets/customizables/pants/pants_2.png")
print(pant2.name)
pant3 = Accessory("Black Jeans", 67.00, "/assets/customizables/pants/pants_3.png")
print(pant3.name)


shirt1 = Accessory("Pink Dress", 67.00, "/assets/customizables/shirts/shirt_1.png")
print(shirt1.name)
shirt2 = Accessory("Night Gown", 67.00, "/assets/customizables/shirts/shirt_2.png")
print(shirt2.name)
shirt3 = Accessory("Pink Shirt", 67.00, "/assets/customizables/shirts/shirt_3.png")
print(shirt3.name)
shirt4 = Accessory("Baby Doll Shirt", 67.00, "/assets/customizables/shirts/shirt_4.png")
print(shirt4.name)
shirtDef = Accessory("Default Gown", 67.00, "/assets/customizables/shirts/shirt.png")
print(shirtDef.name)

shoe1 = Accessory("Sneakers", 67.00, "/assets/customizables/shoes/shoes_1.png")
print(shoe1.name)
shoe2 = Accessory("High Heels", 67.00, "/assets/customizables/shoes/shoes_2.png")
print(shoe2.name)