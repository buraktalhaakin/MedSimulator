import google.generativeai as genai
import json
import time
import os

# --- 1. API ANAHTARINIZI BURAYA GİRİN ---
# Not: API anahtarınızı kodun içinde açık bırakmak yerine Environment Variable kullanmak daha güvenlidir
# ama hızlı test için buraya yazabilirsiniz.
API_KEY = "APIKEY" 
genai.configure(api_key=API_KEY)

# --- 2. AYARLAR ---
generation_config = {
    "temperature": 0.6, 
    "top_p": 0.95,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", 
    generation_config=generation_config,
)

def ikinci_tur_uret(input_dosya, output_dosya, varyasyon_sayisi=2):
    # Dosya yolunu mutlak yola (absolute path) çevirelim ki hata olmasın
    abs_input_path = os.path.abspath(input_dosya)
    abs_output_path = os.path.abspath(output_dosya)

    print(f"📂 Dosya aranıyor: {abs_input_path}")
    
    # Girdi dosyasını oku
    try:
        with open(abs_input_path, 'r', encoding='utf-8') as f:
            kaynak_vakalar = json.load(f)
    except FileNotFoundError:
        print(f"\n❌ HATA: '{abs_input_path}' bulunamadı!")
        print("Lütfen dosya yolunun doğru olduğundan emin olun.")
        return
    except json.JSONDecodeError:
        print(f"\n❌ HATA: JSON dosyası bozuk veya formatı yanlış.")
        return

    genisletilmis_veritabani = []
    # Kaynak vakaları koruyalım
    genisletilmis_veritabani.extend(kaynak_vakalar)

    print(f"--- 🚀 2. TUR BAŞLIYOR ---")
    print(f"Kaynak: {len(kaynak_vakalar)} vaka")
    print(f"Hedef Varyasyon: Her vaka için +{varyasyon_sayisi} yeni vaka.\n")

    for i, vaka in enumerate(kaynak_vakalar, 1):
        mevcut_id = vaka.get('id', f"vaka_{i}")
        tani = vaka.get('gizli_tani', 'Bilinmeyen Tanı')
        
        print(f"[{i}/{len(kaynak_vakalar)}] İşleniyor: {tani} (ID: {mevcut_id})")

        prompt = f"""
        Elimizde şu formatta bir tıbbi vaka var:
        {json.dumps(vaka, ensure_ascii=False)}

        GÖREVİN:
        Bu vakayı temel alarak {varyasyon_sayisi} adet YENİ ve FARKLI vaka türet.
        
        KURALLAR:
        1. TIPKI TIPTA OLDUĞU GİBİ: Hastanın yaşını, cinsiyetini, mesleğini ve ek hastalıklarını değiştir.
        2. SENARYOYU BOZMA: Aynı tanı olsun ama semptomların sunumu (atipik/tipik) değişsin.
        3. ID KURALI: Yeni vakaların ID'si "{mevcut_id}_v1", "{mevcut_id}_v2" şeklinde olsun.
        4. ÇIKTI FORMATI: Sadece ve sadece saf JSON listesi ver. Başka açıklama yazma.

        İstenen JSON Yapısı (Liste İçinde):
        [
            {{ "id": "{mevcut_id}_v1", "hasta_kimlik": {{...}}, "gizli_tani": "{tani}", ... }},
            {{ "id": "{mevcut_id}_v2", "hasta_kimlik": {{...}}, "gizli_tani": "{tani}", ... }}
        ]
        """

        basarili = False
        deneme = 0
        while not basarili and deneme < 3:
            try:
                response = model.generate_content(prompt)
                yeni_vakalar = json.loads(response.text)
                
                if isinstance(yeni_vakalar, list):
                    genisletilmis_veritabani.extend(yeni_vakalar)
                    print(f"   ✅ {len(yeni_vakalar)} yeni varyasyon üretildi.")
                    basarili = True
                else:
                    print("   ⚠️ Model liste döndürmedi, tekrar deneniyor...")
                    deneme += 1
            
            except Exception as e:
                print(f"   ⚠️ Hata (Deneme {deneme+1}): {e}")
                time.sleep(5)
                deneme += 1

        time.sleep(2) 

        # Her 10 vakada bir otomatik kaydet
        if i % 10 == 0:
            with open(abs_output_path, "w", encoding="utf-8") as f:
                json.dump(genisletilmis_veritabani, f, ensure_ascii=False, indent=4)
            print(f"   💾 (Otomatik Kayıt: {len(genisletilmis_veritabani)} vaka)")

    # Final Kayıt
    with open(abs_output_path, "w", encoding="utf-8") as f:
        json.dump(genisletilmis_veritabani, f, ensure_ascii=False, indent=4)
    
    print(f"\n--- 🎉 İŞLEM TAMAMLANDI ---")
    print(f"Başlangıç: {len(kaynak_vakalar)}")
    print(f"Bitiş: {len(genisletilmis_veritabani)}")
    print(f"Dosya Kaydedildi: {abs_output_path}")

# --- ÇALIŞTIR ---
if __name__ == "__main__":
    # Dosya yollarını burada tanımlıyoruz (Windows için r"..." kullanmak en güvenlisidir)
    input_path = r"C:\Users\burak\OneDrive\Belgeler\GitHub\MedSim\case_generators_gemini\medsim_genis_db_v2.json"
    output_path = r"C:\Users\burak\OneDrive\Belgeler\GitHub\MedSim\case_generators_gemini\medsim_genis_db_v3.json"
    
    ikinci_tur_uret(input_path, output_path, varyasyon_sayisi=3)