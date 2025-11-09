class Accessory:
    def __init__(self, id, name, category, price, image):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.image = image
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "image": self.image,
            "backimg": self.backimg,
            "frontimg": self.frontimg
        }

# Hats
hat1 = Accessory(1, "Cowboy", "hat", 50.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437027968764350535/image.png?ex=6911c016&is=69106e96&hm=9ec3df3447f3686223f2ab73e4eae33ce0a55caaf64d464e9539e11f95e2eaf2&=&format=webp&quality=lossless&width=1562&height=1562")
hat2 = Accessory(2, "Witch", "hat", 50.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437028178878140416/image.png?ex=6911c048&is=69106ec8&hm=9817ec3d7c393feb10bbbd299e4c8d2f627cd1900ad7c66e6c3f52fd6c235b4d&=&format=webp&quality=lossless&width=1562&height=1562")

# Hair
hairDef = Accessory(3, "Hair Default", "hair", 0, image="/assets/customizables/hair_top/hair_t.png",
                    frontimg="https://cdn.discordapp.com/attachments/1436786848809615461/1437053428160266271/hair_t.png?ex=6911d7cc&is=6910864c&hm=38be06648fe0846385e13e972f90203bf9b6201bd11a539e18ce4d5ab51d3c00&",
                    backimg="https://cdn.discordapp.com/attachments/1436786848809615461/1437053427036323950/hair_b.png?ex=6911d7cc&is=6910864c&hm=fc96eb5e85c95cc7fb6888cea69fc2f69625990aa9d41ce69b53fabff1cc0646&")
hair1 = Accessory(4, "Hair A", "hair", 75.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437025943079092244/image.png?ex=6911be33&is=69106cb3&hm=2da0a401c08b6a477c65976cfd2246c2b7c5b789072a5c60b05efb2dc422f2eb&=&format=webp&quality=lossless&width=1120&height=1120",
                  frontimg="https://cdn.discordapp.com/attachments/1436786848809615461/1437053428894404678/hair_1t.png?ex=6911d7cc&is=6910864c&hm=9beb17652a2e3fc99b7f5ffce054bf2f08625ed65d8bff8f8cc82291db54d89c&",
                  backimg="https://cdn.discordapp.com/attachments/1436786848809615461/1437053426465767514/hair_1b.png?ex=6911d7cc&is=6910864c&hm=174bf463721462c7722f435d8eff0da18b911f764c9356916b6688d6f1516dda&")
hair2 = Accessory(5, "Hair B", "hair", 75.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437025944127934494/image.png?ex=6911be33&is=69106cb3&hm=3fa866ca4388f2f25ff958491303c2ef2d3940eeb07662cf09030169e3eae86f&=&format=webp&quality=lossless&width=1120&height=1120",
                  frontimg="https://cdn.discordapp.com/attachments/1436786848809615461/1437053428470907040/hair_2t.png?ex=6911d7cc&is=6910864c&hm=4607b9e7578e1cf0e719b06a7c2be32f42bd4336621ae669eec4971ec4c3c102&",
                  backimg="https://cdn.discordapp.com/attachments/1436786848809615461/1437053427434786857/hair_2b.png?ex=6911d7cc&is=6910864c&hm=eca52ae13913c60d83736ffe1242b3450de6c3fdf3adaab2473d91556c28afab&")
hair3 = Accessory(6, "Hair C", "hair", 75.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437025943641133136/image.png?ex=6911be33&is=69106cb3&hm=5e420ebce0c86fde0e09264b881fed1a27148ea5e3a2f765a6033594c48a1c65&=&format=webp&quality=lossless&width=1120&height=1120",
                  frontimg="https://cdn.discordapp.com/attachments/1436786848809615461/1437053427791298703/hair_3t.png?ex=6911d7cc&is=6910864c&hm=87f67614b564e0323efc947c96fe74537c62522b546459e20a699ec191a73b46&",
                  backimg="https://cdn.discordapp.com/attachments/1436786848809615461/1437053426679943288/hair_3b.png?ex=6911d7cc&is=6910864c&hm=93d9b46615ef1d4a56db8d50212911b070bf083bcd6698e6bcab326a79035399&")

# Pants
pant1 = Accessory(7, "Blue Jeans", "pants", 30.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437028255088513196/image.png?ex=6911c05a&is=69106eda&hm=3a4ba63160215fc6ae356d0a3e9ceb91c0f8cd0d7d1371dbf1d1354d9736d352&=&format=webp&quality=lossless&width=1562&height=1562")
pant2 = Accessory(8, "Jean Shorts", "pants", 30.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437028213627944970/image.png?ex=6911c050&is=69106ed0&hm=95156d5ad0e85068e7c226b39a48d1cb0fd2319e18c4d3d87ccbf396d01f6bd7&=&format=webp&quality=lossless&width=1562&height=1562")
pant3 = Accessory(9, "Black Jeans", "pants", 30.00, image="https://media.discordapp.net/attachments/1436786848809615461/1436898715062374480/image.png?ex=691147b5&is=690ff635&hm=e6afbb88932fe9ba9fd0cb5db3e3692ea4f242a8e96d09124629a1cb67d508b1&=&format=webp&quality=lossless&width=1562&height=1562")
pant4 = Accessory(10, "Pink Skirt", "pants", 30.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437027324095631441/Untitled4_20251109024136.png?ex=6911bf7c&is=69106dfc&hm=7ba19d70b194fb6f9613fd8dae76bdf5371e92a80e619d5ac9751c2803e2f7a4&=&format=webp&quality=lossless&width=1562&height=1562")


# Shirts
shirtDef = Accessory(11, "Default Gown", "shirt", 0, image="/assets/customizables/shirts/shirt.png")
shirt1 = Accessory(12, "Pink Dress", "shirt", 45.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437027890247110796/Untitled4_20251108211246.png?ex=6911c003&is=69106e83&hm=33f29c3fd83c2b5c47d675b49a67407030352dc52dccb8424d9b01f8dcecb703&=&format=webp&quality=lossless&width=1354&height=1354")
shirt2 = Accessory(13, "Night Gown", "shirt", 45.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437027889190010970/Untitled4_20251108211151.png?ex=6911c003&is=69106e83&hm=afc4f5ce601128fff7b095fd164881c513af67af48bae5933579b5acce00398a&=&format=webp&quality=lossless&width=1354&height=1354")
shirt3 = Accessory(14, "Pink Shirt", "shirt", 45.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437027683094495323/Untitled4_20251108214421.png?ex=6911bfd2&is=69106e52&hm=5ac01cc4da3257feaab75ed78781569c8feb69fe61342b016d257f2fc21040ca&=&format=webp&quality=lossless&width=1562&height=1562")
shirt4 = Accessory(15, "Baby Doll Shirt", "shirt", 45.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437027509265764434/Untitled4_20251108215856.png?ex=6911bfa8&is=69106e28&hm=517f68797196b7a7f4e49c6346d557da36fee8de8d19774340fa89f76c570d8d&=&format=webp&quality=lossless&width=1562&height=1562")

# Shoes
shoe1 = Accessory(16, "Sneakers", "shoes", 67.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437028285203742782/image.png?ex=6911c061&is=69106ee1&hm=a869ec4a64a101cf5650b66b6a8712634fa690d64ccc71931c0b64cb1ed1ac36&=&format=webp&quality=lossless&width=1562&height=1562")
shoe2 = Accessory(17, "High Heels", "shoes", 67.00, image="https://media.discordapp.net/attachments/1436081196634341396/1437030435589849250/image.png?ex=6911c262&is=691070e2&hm=2706bcaa7b6f36ac901a322058d7726aaff37736ecc5f8fd9289acf1f4c3a823&=&format=webp&quality=lossless&width=1562&height=1562")

ALL_ACCESSORIES = [hat1, hat2, 
                   hair1, hair2, hair3,
                   pant1, pant2, pant3, pant4,
                   shirt1, shirt2, shirt3, shirt4,
                   shoe1, shoe2]

# All accessories list for easy access
print(shoe1.to_dict())