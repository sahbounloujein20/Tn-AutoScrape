import re
import pyodbc

class NettoyagePipeline:
    def process_item(self, item, spider):
        # Nettoyage des chiffres (Prix et Kilométrage)
        if item.get("prix"):
            item["prix"] = re.sub(r"[^\d]", "", str(item["prix"]).strip())
        if item.get("kilometrage"):
            item["kilometrage"] = re.sub(r"[^\d]", "", str(item["kilometrage"]).strip())

        # Correction automatique de l'encodage des caractères (accents UTF-8)
        champs_texte = ["titre", "boite", "energie", "transmission", "cote", "gouvernorat", "puissance"]
        for champ in champs_texte:
            if item.get(champ):
                valeur = str(item[champ]).strip()
                try:
                    valeur = valeur.encode('latin1').decode('utf-8')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass
                item[champ] = valeur

        return item


class SQLServerPipeline:
    def open_spider(self, spider):
        self.conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={spider.settings.get('SQLSERVER_HOST')};"
            f"DATABASE={spider.settings.get('SQLSERVER_DB')};"
            f"Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()
        
        # Utilisation de NVARCHAR pour supporter tous les caractères accentués
        self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='voitures' AND xtype='U')
            CREATE TABLE voitures (
                id INT IDENTITY(1,1) PRIMARY KEY,
                titre NVARCHAR(255),
                prix NVARCHAR(255),
                annee NVARCHAR(255),
                kilometrage NVARCHAR(255),
                boite NVARCHAR(255),
                energie NVARCHAR(255),
                puissance NVARCHAR(255),
                transmission NVARCHAR(255),
                gouvernorat NVARCHAR(255),
                cote NVARCHAR(255),
                lien NVARCHAR(255) UNIQUE,
                image NVARCHAR(255),
                page INT
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""
                INSERT INTO voitures 
                (titre, prix, annee, kilometrage, boite, energie, puissance, transmission, gouvernorat, cote, lien, image, page)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get('titre'), item.get('prix'), item.get('annee'),
                item.get('kilometrage'), item.get('boite'), item.get('energie'),
                item.get('puissance'), item.get('transmission'), item.get('gouvernorat'),
                item.get('cote'), item.get('lien'), item.get('image'), item.get('page')
            ))
            self.conn.commit()
            
        except pyodbc.IntegrityError:
            self.conn.rollback() 
            spider.logger.debug(f"Doublon ignoré : {item.get('lien')}")
        except Exception as e:
            self.conn.rollback()
            spider.logger.error(f"Erreur SQL : {e}")
            
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()