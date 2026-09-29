from urllib.parse import quote_plus

def search_url(platform, query):
    q = quote_plus(query)
    urls = {
        "Amazon": f"https://www.amazon.in/s?k={q}",
        "Flipkart": f"https://www.flipkart.com/search?q={q}",
        "IKEA": f"https://www.ikea.com/in/en/search/?q={q}",
        "Swiggy": f"https://www.swiggy.com/search?query={q}",
        "Zomato": f"https://www.zomato.com/search?query={q}",
        "OYO": f"https://www.oyorooms.com/search?location={q}",
    }
    return urls.get(platform, f"https://www.google.com/search?q={q}+{quote_plus(platform)}")

HOME_CATALOG = [
("LED Ceiling Light","Lighting",1299,"Amazon"),("Modern Ceiling Fan","Cooling",2899,"Flipkart"),
("Compact Study Table","Furniture",4499,"IKEA"),("2-Seater Dining Table","Dining",6999,"IKEA"),
("Accent Wall Art Set","Decor",1599,"Amazon"),("Ergonomic Lounge Chair","Furniture",7999,"Flipkart"),
("Bedside Table Lamp","Lighting",999,"Amazon"),("Storage Cabinet","Storage",5499,"IKEA")]
PARTY_CATALOG = [
("Veg catering package","Catering",350,"Zomato"),("Party snacks package","Catering",220,"Swiggy"),
("Balloon decoration kit","Decoration",1499,"Amazon"),("LED party lights","Decoration",899,"Flipkart"),
("Event venue search","Venue",5000,"OYO"),("Cake and dessert search","Food",900,"Zomato")]
JEWELRY_CATALOG = [
("Minimal gold-tone necklace","Necklace",1299,"Amazon"),("Pearl drop earrings","Earrings",899,"Flipkart"),
("Kundan-style choker","Necklace",2499,"Amazon"),("Elegant bracelet","Bracelet",999,"Flipkart"),
("Oxidised statement earrings","Earrings",699,"Amazon"),("Classic pendant set","Set",1799,"Flipkart")]
