# ♻️ RecycLens
### Smart Vision for Smarter Recycling

> **💡 Mission Statement**
> Improper waste sorting is a major barrier to effective recycling. **RecycLens** leverages computer vision and Generative AI to help users identify, sort, and understand waste materials instantly, supporting **SDG 12 (Responsible Consumption and Production)**.

---

### 🌐 **Live Demo**
👉 **https://recyclens.streamlit.app/**

---

## 🚀 **Overview**

RecycLens addresses the challenge of waste classification by turning your camera into an intelligent recycling assistant. It serves as a functional **MVP (Minimum Viable Product)** demonstrating how AI can solve real-world sustainability problems.

| **Metric** | **Details** |
| :--- | :--- |
| **Type** | Web Application (PWA) |
| **Focus** | Sustainability, AI, Education |
| **Tech** | Streamlit, TensorFlow, Google Gemini |

---

## ✨ **Key Features**

### 🔐 **1. User Experience**
> *Secure and personalized.*
* **Authentication:** Simple, secure login system (Session State management).
* **User Profiles:** Tracks join date, membership status, and activity.
* **Session Security:** Auto-logout capability to protect user data.
* **Password: 1234**

### 📸 **2. AI-Powered Scanner**
> *Instant identification using MobileNetV2.*
* **Real-Time Analysis:** Classifies waste in < 2 seconds.
* **7 Supported Classes:**
    * 🔋 `Battery`
    * 🍏 `Biological`
    * 📦 `Cardboard`
    * 🥂 `Glass`
    * 🔩 `Metal`
    * 📄 `Paper`
    * 🥤 `Plastic`
* **Confidence Threshold:** Filters low-confidence results (<80%) to prevent misinformation.

### 🌍 **3. Eco-Impact Tracker**
> *Gamifying sustainability.*
* **Personal History:** Logs every scan to a user-specific database.
* **Impact Calculator:** Estimates your environmental contribution based on material type.
    * *Formula:* `Total CO2 Saved` = $\sum (Count \times MaterialFactor)$

### 🤖 **4. AI Assistant**
> *Powered by Google Gemini 2.5 Flash.*
* **Floating Chatbot:** A non-intrusive assistant available on the home page.
* **Context-Aware:** Capable of answering specific questions about how to clean or prepare items for recycling.

---

## 🛠️ **Technical Stack**

| Component | Technology Used |
| :--- | :--- |
| **Frontend** | Streamlit (Python) |
| **Computer Vision** | TensorFlow / Keras (CNN) |
| **LLM Engine** | Google Generative AI (Gemini) |
| **Data Handling** | Pandas & NumPy |
| **Image Processing** | PIL (Python Imaging Library) |

---

⚠️ Disclaimer
Note: This application is intended for educational and demonstration purposes. While the model achieves high accuracy (~90%), classification results may vary based on lighting and image quality. It should not be used as the sole basis for industrial waste management decisions.

👩‍💻 Author
Developed by Atiqah Pramudya University Student | AI & Web Development Enthusiast
