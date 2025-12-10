<h1 align="center">🩺 MedSim-AI — Sentetik Tıbbi Vaka Simülasyon Motoru</h1>
<p align="center"><b>Klinik eğitim ve yapay veri üretimi için %100 JSON yapısında, yüksek tutarlıklı vaka üretim motoru.</b></p>

## 📌 Proje Tanımı
MedSim-AI, tıp eğitimi ve yapay zeka araştırmaları için sentetik hasta vakaları üreten güçlü bir pipeline'dır. Büyük öğretici modellerden (MedGemma-27B) elde edilen bilgi, daha küçük student modellere damıtılarak hızlı ve tutarlı vaka üretimi sağlanır. Sistem, halk dili / tıbbi dil ayrımını korur, epidemiolojik uygunluk sağlar ve çıktıları otomatik doğrular.

## 🚀 Temel Özellikler
| Özellik | Açıklama |
|---|---|
| 🧠 Teacher→Student distillation | MedGemma-27B → Gemma-9B/2B LoRA |
| 🌍 Çift dil desteği | Şikayet halk ağzı, notlar akademik terminoloji |
| 📊 Epidemiyolojik uyum | Hastalık→yaş→cinsiyet tutarlılığı otomatik |
| ⚡ vLLM Batch üretim | A100 ile binlerce vaka/dk |
| 🧪 LLM-as-a-Judge | Her vaka skorlanır (%100 JSON valid) |

## 🛠 Mimari Bileşenler
**vLLM Veri Motoru → Distillation & Fine-tuning → Medikal Validasyon (LLM-as-Judge)**  
Teknoloji: vLLM, PagedAttention, Gemma-27B/9B/2B, LoRA–Unsloth, HF Accelerate, JSON Schema doğrulama


### Teknoloji Yığını

| Bileşen | Kullanılan Teknoloji |
|---|---|
| Veri Üretimi | **vLLM**, PagedAttention |
| Model | google/gemma-2-27b-it (Teacher), Gemma-9B/2B-LoRA (Student) |
| Format | %100 Valid JSON Schema |
| Fine-Tuning | LoRA, Unsloth, HF Accelerate |
| Validasyon | Tıbbi Uyum – Vital Mantık – Realizm skoru |

---

## 📂 JSON Çıktı Örneği

```json
{
  "id": "vaka_042",
  "gizli_tani": "Akut Pankreatit",
  "hasta_kimlik": {
    "yas": 45,
    "cinsiyet": "Erkek",
    "sikayet": "Hocam karnımın üst tarafı kuşak gibi ağrıyor, sırtıma vuruyor."
  },
  "anamnez": {
    "sikayet_detaylari": "Epigastrik bölgede ani başlayan, kuşak tarzında yayılan şiddetli ağrı...",
    "ozgecmis": "Kronik alkol kullanımı, Kolelityazis..."
  },
  "bulgular": {
    "fizik_muayene": "Batın distandü, epigastrik hassasiyet mevcut. Rebound (+).",
    "laboratuvar": "Amilaz: 1200 U/L (N<100), Lipaz: 850 U/L, CRP: 45 mg/L",
    "goruntuleme": "Abdominal BT: Pankreasta ödem ve peripankreatik sıvı kolleksiyonu."
  }
}
```
---

## ⚡ Hızlı Başlangıç

### Gereksinimler
- Python **3.10+**
- NVIDIA GPU (**A100 önerilir**, T4 ile Gemma-9B kullanılabilir)
- HuggingFace Token

### Kurulum

```bash
git clone https://github.com/buraktalhaakin/medsimulator.git
cd medsimulator
pip install -r requirements.txt

```

### 1) Sentetik Veri Üretimi (vLLM ile)
A100 GPU üzerinde süper hızlı üretim için:

```bash
python generate_dataset_vllm.py --model "google/gemma-2-27b-it" --count 1000
```

### 2) Kalite Kontrol (Validasyon)

Beta model sonuçlarını veya üretilmiş dataset'i doğrulamak için:
```bash
python validate_model.py --input "beta_results.json"
```

Bu script, vakaları tıbbi tutarlılık açısından analiz eder ve kalite_raporu.png grafiğini oluşturur.
📊 Performans Karşılaştırması
| Özellik | Standart Llama 3 8B | MedSim-AI (Fine-Tuned Gemma) |
|---|---|---|
| JSON Hata Oranı | %15 - %20 | <%1 |
| Tıbbi Tutarlılık | Orta | Yüksek (MedGemma Distilled) |
| Dil Ayrımı | Karışık | Halk Dili / Tıbbi Dil Ayrışmış |
| Üretim Hızı | Standart | 2x Hızlı (Küçük Model) |
⚠️ Yasal Uyarı (Disclaimer)
Bu proje eğitim ve araştırma amaçlıdır. Üretilen tıbbi vakalar yapay zeka tarafından oluşturulmuştur ve gerçek hasta verisi değildir. Klinik karar destek sistemi olarak kullanılmadan önce uzman hekim kontrolünden geçmelidir.
🗺️ Gelecek Planları (Roadmap)
 * [x] vLLM ile toplu veri üretimi
 * [x] Tutarlılık validasyon scripti
 * [ ] Ayırıcı tanı (Differential Diagnosis) modülü
 * [ ] Tedavi planlama ve reçete modülü
 * [ ] Web tabanlı simülasyon arayüzü (Streamlit)

#### Developed by Dr. Burak Talha Akın / Gaye Armut



