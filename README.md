# recommender
Choice Genie


# 🛒 Ontology-Based & ML-Hybrid E-Commerce Recommendation System (Semantic + ML)

### **Final Year Project – Intelligent Product Recommendation Engine**

This project implements a **hybrid recommendation system** that combines:

* **Semantic reasoning** using an RDF/OWL ontology
* **Content-based ML similarity** (TF-IDF + KNN)
* **Dynamic user preference learning**
* **Explainable recommendations** (“Recommended because…”)
* **Interactive frontend** built with HTML, CSS, JS
* **Backend REST API** using Python Flask

The system simulates an e-commerce platform that recommends products with natural-language explanations and learns user preferences over time.

---

## 🚀 Features

### 🔎 **1. Semantic Recommendation**

Uses ontology reasoning from RDF triples:

* Category match
* Rating relevance
* Popularity score
* Budget fit
* Explanation generation

### 🤖 **2. Machine Learning Component**

TF-IDF + KNN content-based similarity:

* Similarity between clicked products
* Used when user clicks a product
* Combines with semantic score

### ⚡ **3. Hybrid Scoring Model**

```
final_score = 0.5 * semantic_score + 0.5 * ml_score
```

### 📘 **4. Explainability**

Every recommendation includes reasons such as:

* “Matches your preferred category”
* “Within your budget”
* “Same brand”
* “Highly rated (4.6★)”

### 🌐 **5. Frontend E-commerce UI**

* Product grid view
* Category filtering
* Click-based recommendation
* Hover overlay explanations
* Fast loading via JS fetch()

#Home Page

<img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/3ba6cdd1-666a-40b0-9c88-ed9e76169445" />

#All Products Display with Reasons to Recommendation breaking **Cold Start**
<img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/20cdc645-d6d9-4a56-aa5d-86897b0713c9" />

#Recommended Products after select one

#Selected Product

<img width="800" height="378" alt="image" src="https://github.com/user-attachments/assets/d63ce938-4ef4-42df-8b87-4457d602c96b" />



#Recommended Products

<img width="800" height="390" alt="image" src="https://github.com/user-attachments/assets/542e2690-6933-4032-b161-57edad6f3817" />




### 💾 **6. Dynamic User Preferences**

Stored in `data/user_prefs.json`.

User preferences update automatically when:

* A user likes/clicks a product
* Budget/min-rating/category preferences saved
* System learns continuously

---

# 📁 Project Structure

```
recommender/
│── backend/
│   ├── app.py                # Flask backend
│   ├── semantic.py           # Semantic reasoning module
│   ├── ml_helper.py          # ML similarity scorer (TF-IDF + KNN)
│   ├── models/               # Stored ML models (.pkl)
│   ├── data/
│   │   └── user_prefs.json   # Dynamic user profile store
│   ├── kg/ttl/
│   │    ├── ontology.ttl     # Ontology file
│   │    └── products.ttl     # RDF product dataset
│   └── venv/                 # Python virtual environment
│
│── frontend/
│   ├── index.html            # UI
│   ├── js/
│   ├── css/
│   └── img/
│
│── eval_recommender.py       # Evaluation script
│── requirements.txt
│── README.md
```

---

# 🧪 Installation & Setup

## 1️⃣ Clone the project

```
git clone https://github.com/yourusername/recommender.git
cd recommender/backend
```

---

# 🔧 Backend Setup (Flask API)

## 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate    # Windows
```

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

If you don't have a requirements file, generate one:

```
pip freeze > requirements.txt
```

## 4️⃣ Run Backend API

```
python app.py
```

Backend default URL:

```
http://127.0.0.1:5000
```

---

# 🌐 Frontend Setup

You can run the frontend locally using Python’s simple HTTP server:

```
cd ../frontend
python -m http.server 3000
```

Frontend URL:

```
http://127.0.0.1:3000
```

---

# 🔗 How Backend & Frontend Communicate

The frontend calls the Flask API using:

```
GET /products
GET /recommendations
POST /like
POST /preferences
```

Example:

```javascript
fetch("http://127.0.0.1:5000/products?category=Computers&user=u1")
```

---

# ▶️ Usage Flow

### 🟦 Step 1 — User visits UI

System loads all products with default explanations.

### 🟧 Step 2 — User clicks a product

Frontend sends:

```
GET /recommendations?based_on=p1009&user=u1
```

Backend:

* Calculates ML similarity
* Generates semantic explanations
* Sends ranked results

### 🟩 Step 3 — User interactions update preferences

```
POST /like
POST /preferences
```

---

# 🧠 Evaluation

Includes:

* Precision/Recall evaluation (`eval_recommender.py`)
* System latency testing
* User Acceptance Testing (30 users)
* Hybrid score benchmarking


<img width="800" height="692" alt="eval" src="https://github.com/user-attachments/assets/02a0762b-cfbb-4133-a2e1-c5d3701e7585" />


---

# 🛠 Technologies Used

| Component      | Technology                     |
| -------------- | ------------------------------ |
| Backend        | Python Flask                   |
| Semantic Layer | RDFLib, SPARQL                 |
| ML Model       | TF-IDF + KNN, Scikit-learn     |
| Storage        | JSON-based preference store    |
| Frontend       | HTML, CSS, JavaScript          |
| Deployment     | Local execution / web application |

---

# 🧩 Future Enhancements

* Integrate with real e-commerce APIs
* Add collaborative filtering
* Transform ML with BERT/Transformers
* Browser extension personal shopping agent
* Deploy cloud backend (AWS / GCP / Render)

---

# 👨‍🎓 Author

**Tharuka Premasiri**
Final Year Undergraduate – BSc (Hons) in Software Engineering
University of Bedfordshire | SLIIT CITY UNI

LinkedIn: *www.linkedin.com/in/tharukapremasiri*

---

# ⭐ Want to support?

Give this repo a **star ⭐ on GitHub** if you found it interesting!



