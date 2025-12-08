import google.generativeai as genai
import json
import time
import os

# --- KONFİGÜRASYON ---
# Buraya Google AI Studio'dan alacağın API key'i yapıştır
API_KEY = "AIzaSyBsofv4SQ1Dpr4E_4uyXmggvAuSsgjp6ac"

genai.configure(api_key=API_KEY)

# Dahiliye asistanı seviyesinde tutarlı olması için model ayarları
generation_config = {
    "temperature": 0.3, # Düşük tutuyoruz ki halüsinasyon görmesin, tıbbi gerçekliğe sadık kalsın.
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json", # Modeli direkt JSON döndürmeye zorluyoruz
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # Hızlı ve ekonomik model
    generation_config=generation_config,
)

def vaka_uret(tani_listesi):
    vaka_veritabani = []
    
    # Sisteme verdiğimiz "rol" ve "kurallar"
    system_instruction = """
    Sen deneyimli bir İç Hastalıkları (Dahiliye) uzmanı ve tıp eğitmenisin.
    Görevin: Tıp öğrencileri ve asistanlar için simülasyon amaçlı vakalar oluşturmak.
    
    Kurallar:
    1. Çıktı kesinlikle belirtilen JSON formatında olmalı.
    2. "gizli_tani" alanı ile "bulgular" (Fizik muayene, Lab, Görüntüleme) %100 tıbbi uyum içinde olmalı.
    3. Hasta profili gerçekçi olmalı (Yaş ve Cinsiyet tanı ile uyumlu olmalı).
    4. "sikayet" kısmı hastanın kendi ağzından, basit bir dille yazılmalı (Tıbbi terim içermemeli).
    5. "sikayet_detaylari" kısmı doktorun sorgusuyla ortaya çıkan, daha detaylı anamnezdir.
    6. Laboratuvar sonuçlarında birimler belirtilmeli ve patolojik değerler tanıya uygun olmalı.
    """

    print(f"Toplam {len(tani_listesi)} adet vaka üretilecek...\n")

    for i, tani in enumerate(tani_listesi, 1):
        print(f"[{i}/{len(tani_listesi)}] '{tani}' tanısı için vaka yazılıyor...")
        
        prompt = f"""
        Lütfen şu tanı için bir vaka oluştur: {tani}
        
        Aşağıdaki JSON şemasını birebir doldur:
        {{
            "id": "vaka_{i:03d}",
            "gizli_tani": "{tani}",
            "hasta_kimlik": {{
                "ad_soyad": "string",
                "yas": integer,
                "meslek": "string",
                "sikayet": "Hastanın ilk başvuruda söylediği cümle"
            }},
            "anamnez": {{
                "sikayet_detaylari": "Sorgulama ile öğrenilen detaylar (süre, vasıf, yayılım vb.)",
                "kronik_hastaliklar": "Varsa hastalıkları yoksa 'Özellik yok'",
                "kullandigi_ilaclar": "Varsa dozları ile birlikte",
                "aile_oykusu": "string",
                "tibbi_ozgecmis": "Operasyonlar, eski yatışlar vb."
            }},
            "bulgular": {{
                "fizik_muayene": "Sistemik muayene bulguları (Vital bulgular dahil)",
                "laboratuvar": "Hemogram, Biyokimya vb. (Sadece tanı ile ilgili anlamlı olanlar)",
                "goruntuleme": "Röntgen, BT, USG vb. rapor sonucu"
            }}
        }}
        """

        try:
            response = model.generate_content(system_instruction + prompt)
            vaka_data = json.loads(response.text)
            vaka_veritabani.append(vaka_data)
            print(" -> Başarılı.")
        except Exception as e:
            print(f" -> Hata oluştu: {e}")
        
        # API limitlerine takılmamak için kısa bir bekleme
        time.sleep(2)

    return vaka_veritabani

# --- ÇALIŞTIRMA KISMI ---

# Hangi konulardan vaka istiyorsan bu listeye ekle
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
    "Akut Miyokard İnfarktüsü",
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
    ]

veritabani = vaka_uret(hedef_tanilar)

# Dosyayı kaydet
dosya_adi = "medsim_vaka_db.json"
with open(dosya_adi, "w", encoding="utf-8") as f:
    json.dump(veritabani, f, ensure_ascii=False, indent=4)

print(f"\nİşlem tamamlandı! '{dosya_adi}' dosyası oluşturuldu.")