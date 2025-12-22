♻️ RecycLens: Smart Vision for Smarter Recycling
RecycLens is an AI-powered web application designed to revolutionize how we handle waste. By leveraging computer vision and generative AI, RecycLens helps users identify, sort, and understand waste materials instantly, supporting SDG 12 (Responsible Consumption and Production).

🌐 Live App: https://recyclens.streamlit.app/

🚀 About The Project
Improper waste sorting is a major barrier to effective recycling. RecycLens addresses this by providing an intelligent, accessible tool that classifies waste in real-time. Whether you are at home, school, or the office, RecycLens turns your camera into a smart recycling assistant.

This project is built as a functional prototype to demonstrate the practical application of Convolutional Neural Networks (CNN) and Large Language Models (LLM) in environmental sustainability.

✨ Key Features
🔐 User Experience
Secure Authentication: User-specific login system to manage sessions.

Personalized Profiles: Track your join date and membership status.

📸 AI-Powered Scanning
Real-Time Classification: Instantly identifies waste using a custom-trained TensorFlow model.

7 Supported Categories: Battery, Biological, Cardboard, Glass, Metal, Paper, and Plastic.

Intelligent Feedback: Displays a "Success" card for clear matches and a "Warning" card if the confidence score is too low (<80%), prompting a rescan.

🌍 Impact Tracking
Personal History Log: Automatically saves your scan history to a database linked to your username.

Eco-Impact Calculator: Estimates the CO₂ savings (kg) and Energy conserved (Wh) based on your recycling history.

📚 Education & Assistance
Context-Aware Learning: Dynamic "Read More" buttons guide you to specific educational pages based on the item detected (e.g., scanning a bottle leads to the Plastic guide).

Integrated Chatbot: A floating AI assistant powered by Google Gemini 2.5 Flash to answer all your recycling questions.

🛠️ Tech Stack
Frontend: Streamlit

Machine Learning: TensorFlow / Keras (MobileNetV2)

AI Integration: Google Generative AI (Gemini)

Data Handling: Pandas & NumPy

Deployment: Streamlit Cloud

⚠️ Disclaimer
This application is intended for educational and demonstration purposes. While the model achieves high accuracy (~90%), classification results may vary based on lighting and image quality. It should not be used as the sole basis for industrial waste management decisions.

👩‍💻 Author
Developed by Atiqah Pramudya University Student | AI & Web Development Enthusiast
