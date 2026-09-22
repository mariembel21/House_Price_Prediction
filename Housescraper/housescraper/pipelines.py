# Define your adapter pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/adapter-pipeline.html


# useful for handling different adapter types with a single interface

import re
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class HousescraperPipeline:

    @staticmethod
    def remove_emojis_and_quotes(text):
        if not text:
            return text

        text = re.sub(r'[^\w\s.,!?;:\-\'\"()\[\]{}]', '', text, flags=re.UNICODE)

        # Remove quotes
        text = text.replace('"', "").replace("'", "").replace("\n", " ").replace("\t", " ").strip()

        return text.strip()

    @staticmethod
    def extract_governorate(ville, source=None):
        if not ville:
            return None
        
        ville = ville.replace("\n", "").replace("\t", "").strip()
        ville = re.sub(r"\bville\b", "", ville, flags=re.IGNORECASE)

        if source == "immobilier":
            parts = [p.strip() for p in ville.split(",")]
            return parts[-1].title() if parts else ville.title()
        elif source == "mubawab":
            ville = re.sub(r"\bin\s*", " in ", ville, flags=re.IGNORECASE)
            if " in " in ville.lower():
                return ville.lower().rsplit(" in ", 1)[1].strip().title()
            return ville.strip().title()
        else:
            return ville.title()


    
    immobilier_type_map = {
       "Appart": "Appart",
       "Villa": "House", 
       "Duplex": "House",   
       "Triplex": "House",       
    }  

    tayara_type_map = {
       "Appartements": "Appart",
       "Maisons et villas": "House",     
    }   

    mubawab_type_map = {
       "Apartment": "Appart",
       "House": "House", 
       "Villa": "House",    
    }   

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        source = adapter.get("source")    
        
        if source == "tayara":
            # Keep only À Vendre
            if adapter.get("type_transaction") != "À Vendre":
                raise DropItem("Tayara item not for sale")

            raw_type = adapter.get("type_bien")
            if raw_type in self.tayara_type_map:
                adapter["type_bien"] = self.tayara_type_map[raw_type]
            else:
                raise DropItem(f"Tayara type not allowed: {raw_type}")
            
        if source == "mubawab":
            raw_type = adapter.get("type_bien")
            adapter["type_bien"] = self.mubawab_type_map[raw_type]
        
        if source == "immobilier":
            raw_type = adapter.get("type_bien")
            if raw_type in self.immobilier_type_map:
                adapter["type_bien"] = self.immobilier_type_map[raw_type]
            else:
                raise DropItem(f"Immobilier type not allowed: {raw_type}")
            
        # Clean titre
        if adapter.get("titre"):
            titre = adapter["titre"]
            titre = self.remove_emojis_and_quotes(titre)
            titre = self.remove_emojis_and_quotes(titre)
            titre = re.sub(r'[\n\r\t]+', ' ', titre)
            titre = re.sub(r'\s+', ' ', titre)
            titre = re.sub(r'&[a-z]+;', '', titre)
            adapter["titre"] = titre.strip()
            
        # Clean prix
        if adapter.get("prix"):
            prix = adapter["prix"].replace("DT", "").replace(" ", "").replace("TND", "").replace("\n", "").replace(",", "").strip()
            try:
                adapter["prix"] = float(prix)
            except ValueError:
                adapter["prix"] = None
        
        # Clean surface
        if adapter.get("surface"):
            surface = adapter["surface"].replace("m", "").replace("\n", "").replace("\t", "").replace("²","").strip()
            try:
                adapter["surface"] = float(surface)
            except ValueError:
                adapter["surface"] = None

        # Clean ville
        if adapter.get("ville"):
            adapter["ville"] = self.extract_governorate(adapter["ville"], source)

        # Clean chambres
        if adapter.get("chambres"):
            try:
                adapter["chambres"] = int(adapter["chambres"].split()[0])
            except ValueError:
                adapter["chambres"] = None

        if adapter.get("chambres") is None:
            raise DropItem(f"No chambre info for {adapter.get('titre')}")
        
        # Clean type_bien
        if adapter.get("type_bien"):
            adapter["type_bien"] = adapter["type_bien"].strip()

        # Drop items with missing fields
        essential_fields = ["chambres", "type_bien", "surface", "prix", "ville", "titre"]
        for f in essential_fields:
            if adapter.get(f) is None:
                raise DropItem(f"Missing {f} for item: {adapter.get('titre')}")
        
        return item
