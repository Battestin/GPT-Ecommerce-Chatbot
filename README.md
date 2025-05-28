# GPT-Ecommerce-Chatbot

This project simulates a customer support chatbot for an e-commerce store, combining GPT-4 Assistants API with custom tools, image recognition, and contextual document handling.

> 🛠 The Flask web app structure was pre-built and provided by Alura as part of the course **"Python GPT: Create Chatbots with AI"**.  
> 🧠 The GPT logic, prompt engineering, persona system, document handling, and tool integration were developed during the course.

---

## 🧩 Key Features

- 🔁 Persistent Assistant with OpenAI’s GPT-4 (Assistants API)
- 📄 Contextual document loading (policies, product list, general info)
- 🎭 Automatic persona selection based on sentiment
- 🧰 Custom tool integration (e.g., promo code validation)
- 🖼️ Image analysis via GPT-4 Vision
- 🌐 Flask + JS frontend for interactive chat + file upload

---

## 🚀 How to Run

1. Clone the repo  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Set your API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Make sure the `/data` folder includes the files:
   - `ecomart_data.txt`
   - `ecomart_policy.txt`
   - `ecomart_products.txt`

5. Run the app:
   ```bash
   python app.py
   ```

6. Open your browser and go to:
   ```
   http://localhost:5000/
   ```

---

## 💬 How It Works

- User sends a message (or image)
- The system determines the **sentiment** and selects a matching **persona**
- GPT-4 chooses the most relevant **document context**
- If an image is sent, it’s processed with **GPT-4 Vision**
- If a tool is triggered (e.g., coupon validation), the assistant uses a **custom function**
- The conversation is stored in a persistent thread

---

## 📦 Tech Stack

- Python + Flask  
- OpenAI API (Assistants, Vision, File Handling)  
- JavaScript frontend  
- HTML/CSS (template provided in course)

---

## 📁 Folder Structure

```
📦 root
 ┣ 📜 app.py
 ┣ 📜 ecomart_assistant.py
 ┣ 📜 helpers.py
 ┣ 📜 select_document.py
 ┣ 📜 select_persona.py
 ┣ 📜 tools_ecomart.py
 ┣ 📜 vision_ecomart.py
 ┣ 📜 requirements.txt
 ┣ 📜 index.js
 ┗ 📁 data/
     ┣ 📄 ecomart_data.txt
     ┣ 📄 ecomart_policy.txt
     ┣ 📄 ecomart_products.txt
```

---

## 📄 License

MIT — use freely, modify boldly, deploy responsibly.
