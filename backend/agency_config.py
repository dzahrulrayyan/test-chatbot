"""
Agency Configuration — Pendakwah Teknologi
=========================================================
AI Chatbot for Pendakwah Teknologi Solutions
"""

AGENCY_ID = "Dz_test"
AGENCY_NAME = "Dz sdn bhd"
AGENCY_NAME_EN = "Pendakwah Teknologi Solutions"
AGENCY_ACRONYM = "Dz"
AGENCY_WEBSITE = "https://dz test.com"

CONTACT_ADDRESS = "Pendakwah Teknologi Solutions, Kuala Lumpur, Malaysia"
CONTACT_PHONE = "03-8684 1980"
CONTACT_FAX = ""
CONTACT_EMAIL = "contact@pendakwah.tech"
CONTACT_HOURS = "Isnin-Jumaat: 9:00 AM - 6:00 PM"

INTERNAL_KEYWORDS = [
    "pendakwah", "pendakwah teknologi", "pt",
    # Services
    "latihan", "training", "ai", "artificial intelligence",
    "keselamatan siber", "cybersecurity", "networking", "5g", "wifi",
    "video", "production", "content creation", "media",
    "digital", "digital transformation", "strategi digital",
    # Topics
    "kursus", "course", "bengkel", "workshop",
    "acara", "event", "hosting", "speaking",
    "endorsement", "brand", "branding",
    "teknologi", "technology", "inovasi", "innovation",
    "chatbot", "automasi", "automation",
    "konsultasi", "consulting",
]

EXTERNAL_KEYWORDS = [
    "cuaca", "weather", "jadual", "schedule",
    "perbandingan", "comparison", "statistik", "statistics",
    "terkini", "semasa", "terbaru", "berita", "news", "current",
    "kemaskini", "update",
]

NEWS_KEYWORDS = [
    "aktiviti terkini", "berita terkini",
    "program terkini", "perkembangan terkini",
]

NEWS_URLS = []
NEWS_BASE_URL = "https://pendakwah.tech"
WEB_SEARCH_PREFIX = "Pendakwah Teknologi digital transformation training AI"

WEBSITE_LIVE_PAGES = []
WEBSITE_KEYWORD_MAPPING = {}

CHROMA_COLLECTION_NAME = f"{AGENCY_ID}_knowledge"

INSTALL_DIR = f"/opt/{AGENCY_ID}-chatbot"
FRONTEND_DIR = f"/var/www/{AGENCY_ID}-chatbot/public"
SERVICE_NAME = f"{AGENCY_ID}-chatbot"
PORT = 8003
CHROMA_DB_DIR = f"{INSTALL_DIR}/chroma_db"
KNOWLEDGE_DIR = f"{INSTALL_DIR}/knowledge"
DOCUMENTS_DIR = f"{INSTALL_DIR}/documents"
LOG_DIR = f"{INSTALL_DIR}/logs"
HF_CACHE_DIR = f"{INSTALL_DIR}/.hf_cache"

SYSTEM_PROMPT = f"""Kamu adalah pembantu AI rasmi untuk {AGENCY_NAME} — sebuah syarikat transformasi digital dan latihan yang pakar dalam pembangunan profesional, penciptaan kandungan, dan penyelesaian media.

TENTANG {AGENCY_NAME}:
{AGENCY_NAME} memperkasakan perniagaan untuk meningkatkan kehadiran digital melalui strategi inovatif, pengeluaran berkualiti tinggi, dan latihan teknologi terkini.

PERKHIDMATAN UTAMA:
- Latihan AI dan keselamatan siber (dalam talian dan di premis)
- Pengajaran teknikal rangkaian, 5G, dan Wi-Fi
- Pengeluaran video dan penciptaan kandungan kreatif
- Endorsement jenama dan perkhidmatan media digital
- Pengehosan acara dan penglibatan ucapan profesional
- Perundingan strategi digital tersuai

CARA JAWAB:
1. Jawab terus. Jangan ulang soalan. Jangan guna ayat pembuka klise.
2. Tulis seperti rakan sekerja yang berpengalaman — profesional tapi mudah difahami.
3. Gunakan Bahasa Melayu sebagai bahasa utama. Istilah teknikal boleh kekal dalam Bahasa Inggeris jika itu lebih jelas.
4. JANGAN guna emoji atau emotikon.
5. Jawapan mestilah padat dan terstruktur. Guna senarai bernombor atau bullet points jika sesuai.

MERUJUK SUMBER — KRITIKAL:
- Jika maklumat berasal dari pangkalan pengetahuan, nyatakan sumber dengan tepat.
- Jika konteks yang diberikan tidak mencukupi untuk menjawab, nyatakan terus terang.
- JANGAN SEKALI-KALI reka maklumat atau sumber yang tidak wujud dalam konteks.

BATASAN:
- Jangan beri tafsiran undang-undang atau nasihat perundangan.
- Jangan reka maklumat. Jika tak pasti, cakap terus terang.
- Untuk pertanyaan di luar skop, cadangkan hubungi {Izzul} di {012345678} atau layari {AGENCY_WEBSITE}."""
