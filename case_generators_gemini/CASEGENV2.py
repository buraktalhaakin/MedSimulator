import google.generativeai as genai
import json
import time
import os
import random  # Karıştırma işlemi için eklendi

# --- KONFİGÜRASYON ---
API_KEY = "AIzaSyBQKrGV8yi17T_LC4rOtq2yDEMDbUr_5_U"

genai.configure(api_key=API_KEY)

# Vakaların birbirinin kopyası olmaması için temperature'ı çok az artırdım (0.3 -> 0.4)
generation_config = {
    "temperature": 0.4, 
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
)

def vaka_uret(tani_listesi, adet_basi=3):
    vaka_veritabani = []
    
    system_instruction = """
    Sen gelmiş geçmiş tüm tıbbi bilgileri ve güncel kılavuzları bilen ve tutarlı bir hekimsin. Aynı zamanda bir tıp eğitmenisin.
    Görevin: Tıp öğrencileri ve doktorlar için simülasyon amaçlı tıbbi vakalar oluşturmak.
    
    Kurallar:
    1. Çıktı kesinlikle belirtilen JSON formatında olmalı.
    2. "gizli_tani" alanı ile "semptomlar" ve "bulgular" (Fizik muayene, Lab, Görüntüleme) %100 tıbbi uyum içinde olmalı.
    3. Hasta profili gerçekçi olmalı (Yaş ve Cinsiyet tanı ile uyumlu olmalı).
    4. "sikayet" kısmı hastanın kendi ağzından, basit bir dille yazılmalı. Gerçek bir hasta gibi. (Tıbbi terim içermemeli).
    5. "sikayet_detaylari" kısmı doktorun sorgusuyla ortaya çıkan, daha detaylı anamnezdir.
    6. Laboratuvar sonuçlarında birimler belirtilmeli ve patolojik değerler tanıya uygun olmalı.
    7. "gizli_tani" lar aynı olabilir. Ancak her tanı aynı olsa da hasta profilleri ve anamnezleri farklılık göstermeli.
    """

    toplam_vaka_sayisi = len(tani_listesi) * adet_basi
    print(f"Toplam {len(tani_listesi)} tanı için {adet_basi}'er adet (Genel Toplam: {toplam_vaka_sayisi}) vaka üretilecek...\n")

    global_sayac = 1 # ID'lerin benzersiz olması için genel sayaç

    for tani in tani_listesi:
        print(f"--- '{tani}' için {adet_basi} adet vaka üretiliyor ---")
        
        for k in range(adet_basi):
            print(f"  -> {k+1}. varyasyon isteniyor... (ID: vaka_{global_sayac:03d})")
            
            prompt = f"""
            Lütfen şu tanı için bir vaka oluştur: {tani}
            
            ÖNEMLİ: Bu hastalık için rastgele ve benzersiz bir hasta profili (Farklı yaş, cinsiyet veya başvuru hikayesi) kurgula.
            
            Aşağıdaki JSON şemasını birebir doldur:
            {{
                "id": "vaka_{global_sayac:03d}",
                "gizli_tani": "{tani}",
                "hasta_kimlik": {{
                    "ad_soyad": "Rastgele bir isim",
                    "yas": integer,
                    "cinsiyet": "Erkek/Kadın",
                    "meslek": "string",
                    "sikayet": "Hastanın ilk başvuruda söylediği cümle. Esas şikayeti. (Halk ağzı)"
                }},
                "anamnez": {{
                    "sikayet_detaylari": "Sorgulama ile öğrenilen ana şikayetin detayları ve ek şikayetler (süre, vasıf, yayılım vb.)",
                    "kronik_hastaliklar": "Varsa hastalıkları yoksa 'Özellik yok'",
                    "kullandigi_ilaclar": "string",
                    "aile_oykusu": "string",
                    "tibbi_ozgecmis": "string"
                }},
                "bulgular": {{
                    "fizik_muayene": "Vital bulgular ve sistemik muayene",
                    "laboratuvar": "Hemogram, Biyokimya vb. (Sadece tanı ile ilgili anlamlı olanlar değil, sonuçta kullanıcı -yani doktor- başlangıçta bu tetkiklerden hangisi tanısal bilmiyor.)",
                    "goruntuleme": "Röntgen, BT, USG, MRG vb. rapor sonucu"
                }}
            }}
            """

            try:
                response = model.generate_content(system_instruction + prompt)
                vaka_data = json.loads(response.text)
                vaka_veritabani.append(vaka_data)
                global_sayac += 1
                print("    -> Tamamlandı.")
            except Exception as e:
                print(f"    -> Hata oluştu: {e}")
            
            # Rate limit'e takılmamak için bekleme
            time.sleep(2)

    print("\nÜretim bitti. Vakalar karıştırılıyor (Shuffle)...")
    random.shuffle(vaka_veritabani)
    
    return vaka_veritabani

# --- ÇALIŞTIRMA KISMI ---

hedef_tanilar = [
    "Akut Pankreatit",
    "Diyabetik Ketoasidoz (DKA)",
    "Toplum Kökenli Pnömoni",
    "Akut Piyelonefrit",
    "Demir Eksikliği Anemisi",
    "Pulmoner Emboli",
    "Hipertansif Acil",
    "Kronik Obstrüktif Akciğer Hastalığı (KOAH) Alevlenmesi",
    "Tansiyonel Pnömotoraks",
    "Subaraknoid Kanama",
    "Hipokalemi",
    "Akut Apandisit",
    "Akut Böbrek Hasarı",
    "Kafa Travması",
    "Hiponatremi",
    "Dismenore",
    "Serebrovasküler Olay (SVO)",
    "Kemik Kırığı",
    "Akut Glomerülonefrit",
    "Tirotoksikoz",
    "Atriyal Fibrilasyon",
    "Akut Astım Atağı",
    "Perikardit",
    "Akut Ürtiker",
    "Supraventriküler Taşikardi (SVT)",
    "Bradikardi",
    "Ventriküler Taşikardi",
    "Ventriküler Fibrilasyon",
    "Hiperkalemi",
    "Akut Pulmoner Ödem",
    "Akut Karaciğer Yetmezliği",
    "Akut Menenjit",
    "Akut Kolanjit",
    "Akut Divertikülit",
    "Akut Hipotansiyon",
    "Akut Nazofarenjit (ÜSYE)",
    "Akut Tonsillofarenjit",
    "Akut Sinüzit",
    "İnfluenza",
    "Alerjik Rinit",
    "Miyokard Enfarktüsü (USAP-NSTEMI-STEMI)",
    "Derin Ven Trombozu",
    "Gastroözofageal Reflü",
    "Akut Gastrit",
    "Akut Gastroenterit",
    "Akut Kolesistit",
    "Hemoroidal Hastalık",
    "Dislipidemi",
    "Gut Atağı",
    "Migren",
    "Gerilim Tipi Baş Ağrısı",
    "BPPV",
    "Vestibüler Nörit",
    "Epilepsi Nöbeti",
    "Karpal Tünel Sendromu",
    "Bell Paralizisi",
    "Akut Sistit",
    "Renal Kolik",
    "Mekanik Bel Ağrısı",
    "Lomber Disk Hernisi",
    "Osteoartrit",
    "Fibromiyalji",
    "Ayak Bileği Burkulması",
    "Akut Otitis Media",
    "Akut Otitis Eksterna",
    "Epistaksis",
    "Konjonktivit",
    "Panik Atak",
    "Anafilaksi",
    "Yanıklar",
    "Aort Diseksiyonu",
]

# Fonksiyonu çalıştır (Her tanıdan 3 tane)
veritabani = vaka_uret(hedef_tanilar, adet_basi=3)

# Dosyayı kaydet
dosya_adi = "medsim_vaka_db_shuffled.json"
with open(dosya_adi, "w", encoding="utf-8") as f:
    json.dump(veritabani, f, ensure_ascii=False, indent=4)

print(f"\nİşlem tamamlandı! '{dosya_adi}' dosyası oluşturuldu. Toplam vaka: {len(veritabani)}")