# 🩺 MedSim : AI Destekli Tıbbi Vaka Simülasyonu

*MedSim*, tıp öğrencileri, intörnler ve doktorlar için tasarlanmış, yapay zeka tabanlı interaktif bir klinik vaka simülasyon aracıdır. Google Gemini modellerini kullanarak her seferinde benzersiz, tutarlı ve eğitici hasta senaryoları oluşturur.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)

## 🎯 Özellikler

* *Sonsuz Vaka Senaryosu:* Dahiliye, Pediatri, Genel Cerrahi ve diğer branşlarda rastgele veya spesifik vakalar oluşturun.
* *Gerçekçi Hasta Rolü:* Yapay zeka, sadece şikayetini söyleyen ve sorulara kısa/net cevaplar veren gerçek bir hasta gibi davranır.
* *Klinik Araçlar:*
    * 💓 *Vitaller:* Tansiyon, Nabız, Ateş, SpO2 vb. ölçümü.
    * 🩺 *Fizik Muayene:* Sistem bazlı muayene bulguları
    * 🧪 *Laboratuvar:* Hemogram, Biyokimya, Kan Gazı vb. sonuçları
    * 🩻 *Görüntüle:* Direkt grafi, BT, MR, USG raporları.
* *Anlık Geri Bildirim:* Koyduğunuz tanı veya verdiğiniz order (tedavi), güncel kılavuzlara göre yapay zeka tarafından anında değerlendirilir.
* *Güvenli Kullanım:* API anahtarı sunucuda saklanmaz, sadece oturum süresince RAM'de tutulur.

## 🚀 Canlı Demo

Projeyi tarayıcınızda kurulum yapmadan denemek için tıklayın:
*https://medsim-alpha.streamlit.app/*

(Not: Uygulamayı kullanmak için kendi Google Gemini API anahtarınıza ihtiyacınız vardır.)

## 💻 Kurulum (Local)

Bu projeyi kendi bilgisayarınızda çalıştırmak isterseniz:

1.  *Repoyu klonlayın:*
    bash
    git clone [https://github.com/ClesteA/MedSim.git](https://github.com/ClesteA/MedSim.git)
    cd MedSim
    

2.  *Gerekli kütüphaneleri yükleyin:*
    bash
    pip install -r requirements.txt
    

3.  *Uygulamayı başlatın:*
    bash
    streamlit run medsim.py
    

## 🔑 API Anahtarı Hakkında

Bu uygulama *Google Gemini API* kullanır. 
* Anahtarınız kod içinde saklanmaz.
* Arayüzdeki kutucuğa girdiğinizde sadece o oturum için kullanılır.
* Ücretsiz bir API anahtarı almak için: [Google AI Studio](https://aistudio.google.com/app/apikey)

## ⚠ Yasal Uyarı (Disclaimer)

Bu proje *sadece eğitim ve simülasyon amaçlıdır*. 
* Sunulan veriler, tanılar ve tedavi önerileri yapay zeka tarafından üretilmektedir ve gerçek tıbbi tavsiye yerine geçmez.
* Gerçek hasta bakımında kullanılmamalıdır.
* Her zaman güncel tıbbi kılavuzlara ve uzman görüşüne başvurunuz.

---
Geliştirici: ClesteA
