# E-Commerce Next.js Platform - Technical Interview Guide

## 📋 Project Overview

**Bharat Int Udyog** is a **modern e-commerce storefront** for a construction materials business, built with **Next.js 16** and **React 19**. The platform specializes in selling construction bricks with an intelligent **ML-powered recommendation system**.

### Core Purpose
- Provide an online storefront for construction brick products
- Enable user authentication and account management
- Manage shopping cart and checkout operations
- **AI-powered brick recommendations** based on project requirements
- Admin dashboard for order management

---

## 🏗️ Technology Stack

### Frontend
- **Framework**: Next.js 16.1.7 (App Router)
- **Language**: TypeScript 5
- **UI Library**: React 19.2.3
- **Styling**: Tailwind CSS 4
- **UI Components**: Lucide React (icons), Sonner (notifications)

### Backend
- **Runtime**: Node.js with Next.js API Routes
- **Database**: MongoDB (with Mongoose ODM)
- **Authentication**: JWT + bcryptjs
- **ML Service**: FastAPI (Python) for recommendations

### ML/Recommendation Engine
- **Framework**: FastAPI (Python)
- **ML Algorithm**: Random Forest Classifier (scikit-learn)
- **Model Storage**: joblib
- **Feature Engineering**: sklearn.preprocessing (OneHotEncoder, SimpleImputer)

---

## 🗂️ Project Structure & Architecture

### Core Directories

```
E_Commerce_Next_JS/
├── app/                    # Next.js App Router (pages + API routes)
│   ├── api/               # Backend API endpoints
│   │   ├── auth/          # Authentication routes
│   │   ├── products/      # Product catalog API
│   │   ├── cart/          # Cart operations
│   │   ├── orders/        # Order management
│   │   ├── recommend/     # ML recommendation endpoint ⭐
│   │   └── ...
│   ├── layout.tsx         # Root layout wrapper
│   ├── page.tsx           # Homepage
│   ├── shop/              # Product listing page
│   ├── products/[id]/     # Dynamic product details
│   ├── cart/              # Shopping cart UI
│   ├── checkout/          # Checkout flow
│   ├── orders/            # User's order history
│   ├── profile/           # User profile page
│   └── admin/             # Admin dashboard
│
├── components/            # Reusable React components
│   ├── Header.tsx         # Navigation bar
│   ├── Footer.tsx         # Footer section
│   ├── CartModal.tsx      # Shopping cart modal
│   ├── ProductCard.tsx    # Individual product card
│   ├── RecommendationWidget.tsx  # ML demo form ⭐
│   ├── LoginSignupModal.tsx
│   ├── home/              # Homepage specific components
│   └── ...
│
├── context/               # React Context for state management
│   ├── AuthContext.tsx    # User authentication state
│   └── CartContext.tsx    # Shopping cart state
│
├── lib/                   # Shared utilities & database
│   ├── mongodb.ts         # MongoDB connection
│   ├── auth-db.ts         # Authentication DB utilities
│   └── models/            # Mongoose schemas
│       ├── User.ts        # User model
│       ├── Order.ts       # Order model
│       ├── OTP.ts         # OTP verification
│       └── Contact.ts     # Contact form submissions
│
├── data/                  # Static/seed data
│   ├── products.ts        # Brick product catalog
│   └── testimonials.ts    # Customer testimonials
│
├── ml/                    # Machine Learning pipeline ⭐
│   ├── api.py            # FastAPI server
│   ├── recommendation_pipeline.py  # ML logic
│   ├── verify_api.py     # API testing script
│   ├── models/           # Trained models
│   │   └── brick_recommender.joblib  # RandomForest model
│   ├── data/             # Training data
│   │   └── brick_recommendations.csv
│   └── tests/            # ML tests
│
├── public/               # Static assets
│   └── images/          # Product images
│
├── scripts/              # Build/seed scripts
│   ├── seed-db.ts       # Database initialization
│   └── seed-admin.ts    # Admin user creation
│
└── types/               # TypeScript type definitions
    └── index.ts         # Shared interfaces
```

---

## 🤖 ML Recommendation System (Technical Deep Dive) ⭐

### How It Works - End-to-End

The recommendation system is the **most interesting technical component**. Here's how it works:

### 1️⃣ **Frontend: RecommendationWidget Component** 
   - **Location**: `/components/RecommendationWidget.tsx`
   - **What it does**: Interactive form to collect project parameters
   - **Parameters collected**:
     - `constructionType`: Residential / Commercial / Industrial
     - `budget`: Total project budget (₹)
     - `requiredStrength`: Low / Medium / High
     - `durability`: Low / Medium / High
     - `brickPrice`: Price per brick (₹)
     - `brickQuality`: Basic / Standard / Premium
     - `customerPreference`: Cost / Budget / Durability / Aesthetic
     - `previousOrders`: Customer's past order count

### 2️⃣ **Form Submission Flow**
```typescript
// User fills form → clicks Submit
// Frontend converts string inputs to numbers
const payload = {
  constructionType: 'Residential',      // string
  budget: 10000,                        // number
  requiredStrength: 'High',             // string
  // ... other fields
};

// POST request to Next.js API endpoint
fetch('/api/recommend', { method: 'POST', body: JSON.stringify(payload) })
```

### 3️⃣ **Next.js API Bridge** 
   - **Location**: `/app/api/recommend/route.ts`
   - **What it does**: 
     - Receives form data from frontend
     - Forwards to Python ML service
     - Returns prediction result
   
```typescript
// API receives POST request
const response = await fetch(`${ML_SERVICE_URL}/recommend`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),  // Forward to FastAPI
});
```

### 4️⃣ **Python ML Service (FastAPI)**
   - **Location**: `/ml/api.py`
   - **Endpoint**: `POST /recommend`
   - **What it does**:
     - Validates incoming data with Pydantic
     - Calls the recommendation pipeline
     - Returns predictions with probabilities

```python
@app.post('/recommend')
def recommend(request: RecommendationRequest):
    payload = request.model_dump()
    return predict_recommendation(payload)
```

### 5️⃣ **ML Pipeline - The Brain** ⭐⭐⭐
   - **Location**: `/ml/recommendation_pipeline.py`
   - **Algorithm**: Random Forest Classifier
   - **Key Steps**:

#### **A) Feature Engineering**
```python
# Input features converted to feature vector
FEATURE_COLUMNS = [
    'constructionType',      # Categorical
    'budget',               # Numeric
    'requiredStrength',     # Categorical
    'durability',           # Categorical
    'brickPrice',           # Numeric
    'brickQuality',         # Categorical
    'customerPreference',   # Categorical
    'previousOrders',       # Numeric
]

# Example: 
# ['Residential', 10000, 'High', 'High', 9, 'Premium', 'Durability', 3]
```

#### **B) Data Preprocessing**
```python
preprocessor = ColumnTransformer(
    transformers=[
        # Numeric features: fill missing with median
        ('num', SimpleImputer(strategy='median'), 
         ['budget', 'brickPrice', 'previousOrders']),
        
        # Categorical features: encode as one-hot
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore')),
        ]), categorical_features),
    ]
)
```

**What happens**:
- **Numeric columns** → Missing values replaced with median
- **Categorical columns** → Converted to one-hot encoding (each category becomes a binary column)

#### **C) Random Forest Model**
```python
clf = Pipeline(
    steps=[
        ('preprocess', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=200,      # 200 decision trees
            max_depth=8,           # Tree depth limit
            random_state=42,       # Reproducibility
            n_jobs=-1              # Use all CPU cores
        )),
    ]
)

# Training
clf.fit(X_train, y_train)  # Learn patterns from historical data
```

**How Random Forest Works**:
1. Creates 200 independent decision trees
2. Each tree learns different patterns from the data
3. For prediction: all trees "vote" on the best brick type
4. Final prediction = majority vote result
5. Confidence = how many trees agreed

#### **D) Prediction Output**
```python
def predict_recommendation(payload):
    features = pd.DataFrame([build_feature_vector(payload)], 
                            columns=FEATURE_COLUMNS)
    
    prediction = model.predict(features)[0]        # Predicted class
    probabilities = model.predict_proba(features)[0]  # Confidence scores
    classes = model.classes_                       # All brick types
    
    # Example output:
    # {
    #   'prediction': 'प्रथम श्रेणी सामान्य ईंट',
    #   'confidence': 0.92,
    #   'probabilities': {
    #     'प्रथम श्रेणी सामान्य ईंट': 0.92,
    #     'द्वितीय श्रेणी ईंट': 0.06,
    #     'तृतीय श्रेणी ईंट': 0.02,
    #   }
    # }
```

### 6️⃣ **Training Data Format**

The model learns from historical data in CSV format:

```csv
constructionType,budget,requiredStrength,durability,brickPrice,brickQuality,customerPreference,previousOrders,recommendedBrick
Residential,12000,High,High,9,Premium,Durability,3,प्रथम श्रेणी सामान्य ईंट
Residential,10000,Medium,Medium,8,Standard,Budget,2,द्वितीय श्रेणी ईंट
Commercial,9000,Medium,Medium,8,Standard,Budget,1,द्वितीय श्रेणी ईंट
Industrial,13000,High,High,10,Premium,Durability,5,प्रथम श्रेणी सामान्य ईंट
```

The model learns patterns like:
- High budget + High requirements → Premium brick recommendation
- Low budget + Commercial → Budget brick option
- Industrial + Durability focus → Premium brick

### 7️⃣ **Complete Request-Response Flow**

```
┌─────────────────────────────────────────────────────────┐
│ Frontend: User fills RecommendationWidget form          │
└─────────────────┬───────────────────────────────────────┘
                  │ Form submission
                  ▼
┌─────────────────────────────────────────────────────────┐
│ Next.js API: /api/recommend                              │
│ - Receives: { constructionType, budget, ... }           │
│ - Forwards to ML service                                │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP POST
                  ▼
┌─────────────────────────────────────────────────────────┐
│ FastAPI ML Service: POST /recommend                      │
│ - Validates Pydantic schema                             │
│ - Calls predict_recommendation()                        │
└─────────────────┬───────────────────────────────────────┘
                  │ Python function call
                  ▼
┌─────────────────────────────────────────────────────────┐
│ Recommendation Pipeline: predict_recommendation()        │
│ 1. Build feature vector from input                      │
│ 2. Create DataFrame with proper column names            │
│ 3. Pass through sklearn Pipeline:                       │
│    - Preprocessing (imputation, encoding)              │
│    - Random Forest inference                            │
│ 4. Extract prediction + probabilities                   │
│ 5. Return JSON response                                 │
└─────────────────┬───────────────────────────────────────┘
                  │ JSON result
                  ▼
┌─────────────────────────────────────────────────────────┐
│ FastAPI Returns: { prediction, confidence, ... }        │
└─────────────────┬───────────────────────────────────────┘
                  │ JSON response
                  ▼
┌─────────────────────────────────────────────────────────┐
│ Next.js API returns to Frontend                         │
└─────────────────┬───────────────────────────────────────┘
                  │ JSON response
                  ▼
┌─────────────────────────────────────────────────────────┐
│ Frontend: Display recommendation result to user         │
└─────────────────────────────────────────────────────────┘
```

### Why This Architecture? 🎯

| Aspect | Reason |
|--------|--------|
| **Separate ML Service** | Isolates computation-heavy ML from web server; enables scaling |
| **Random Forest** | Handles mixed data types (numeric + categorical); fast prediction; interpretable |
| **Pipeline Pattern** | Ensures preprocessing is applied consistently in training & prediction |
| **Joblib Model Storage** | Serializes entire fitted model + preprocessing; quick loading |
| **FastAPI** | Lightweight Python web framework; async support; automatic Pydantic validation |
| **Next.js Bridge** | Hides ML service URL; adds authentication layer; enables caching |

---

## 🔐 Authentication System

### Components

1. **Backend**:
   - `/lib/auth-db.ts`: Utility functions for user DB operations
   - `/app/api/auth/login`: Email/password authentication
   - `/app/api/auth/signup`: User registration
   - `/app/api/auth/send-otp`: OTP generation for phone auth
   - `/app/api/auth/verify-otp`: OTP verification
   - **Password Hashing**: bcryptjs (salted + hashed)

2. **Frontend** (React Context):
   - `/context/AuthContext.tsx`: Central auth state management
   - Provides: `login()`, `signup()`, `logout()`, `loginWithPhone()`
   - Stores user in localStorage for persistence

### User Model (MongoDB)
```typescript
interface IUser {
  name: string;
  email?: string;           // Optional, sparse unique
  phone?: string;           // Optional, sparse unique
  passwordHash?: string;    // bcryptjs hash
  isAdmin?: boolean;        // Admin flag
  createdAt: Date;
}
```

---

## 🛒 Shopping Cart System

### State Management (React Context)

**File**: `/context/CartContext.tsx`

**Features**:
- Per-user cart storage (separate localStorage key per user)
- Guest cart support (for unauthenticated users)
- Operations: `addToCart()`, `removeFromCart()`, `updateQuantity()`, `clearCart()`
- Persistence: Auto-saves to localStorage when cart changes
- Syncing: Reloads cart when user logs in/out

```typescript
// Cart stored separately per user
const cartKey = (userId) => userId ? `bharat-cart-${userId}` : 'bharat-cart-guest'
```

---

## 📦 Product Catalog

**Location**: `/data/products.ts`

**Product Details**:
```typescript
interface Product {
  id: string;
  name: string;           // Hindi + English
  description: string;
  price: number;          // Current price
  comparePrice: number;   // Original price (for discount display)
  image: string;          // Image URL
  category: string;       // Brick grade/type
  rating: number;         // Star rating (1-5)
  reviews: number;        // Review count
  inStock: boolean;
}
```

**Available Bricks**:
- प्रथम श्रेणी सामान्य ईंट (Grade 1 - Premium)
- द्वितीय श्रेणी ईंट (Grade 2 - Standard)
- तृतीय श्रेणी ईंट (Grade 3 - Budget)
- चतुर्थ श्रेणी ईंट (Grade 4 - Fill/Utility)

---

## 🔗 API Routes Overview

### Public Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/products` | GET | Fetch all products or filter by category |
| `/api/recommend` | POST | Get ML brick recommendation ⭐ |
| `/api/auth/login` | POST | Email/password authentication |
| `/api/auth/signup` | POST | Register new user |
| `/api/auth/send-otp` | POST | Send OTP to phone |
| `/api/auth/verify-otp` | POST | Verify OTP & authenticate |

### Authenticated Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/cart` | POST/GET | Add/retrieve cart items |
| `/api/orders` | GET/POST | View/create orders |
| `/api/checkout` | POST | Complete purchase |
| `/api/contact` | POST | Contact form submission |

### Admin Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/admin/orders` | GET | View all orders |

---

## 🗄️ Database Models

### 1. User Model
```typescript
{
  name: String (required),
  email: String (unique, sparse),
  phone: String (unique, sparse),
  passwordHash: String,
  isAdmin: Boolean (default: false),
  createdAt: Date,
  updatedAt: Date
}
```

### 2. Order Model
```typescript
{
  userId: ObjectId (ref: User),
  items: Array<{
    productId: String,
    quantity: Number,
    price: Number
  }>,
  total: Number,
  status: String (pending/confirmed/shipped/delivered),
  createdAt: Date
}
```

### 3. OTP Model
```typescript
{
  phone: String (unique),
  otp: String,
  expiresAt: Date,
  attempts: Number
}
```

### 4. Contact Model
```typescript
{
  name: String,
  email: String,
  phone: String,
  message: String,
  status: String (new/responded),
  createdAt: Date
}
```

---

## 🚀 Deployment & Environment

### Required Environment Variables
```env
MONGODB_URI=mongodb+srv://...
JWT_SECRET=your-secret-key
ML_SERVICE_URL=http://127.0.0.1:8000  # Python ML service
```

### Running the Project

```bash
# Install dependencies
npm install

# Start Next.js dev server (port 3000)
npm run dev

# In another terminal, start ML service
cd ml
pip install -r requirements.txt
python -m uvicorn api:app --reload --port 8000
```

---

## 📊 Key Technical Decisions

| Decision | Why |
|----------|-----|
| **Next.js 16** | Full-stack framework; SSR + API routes; built-in optimization |
| **TypeScript** | Type safety; better IDE support; fewer runtime errors |
| **Tailwind CSS** | Utility-first; responsive design; rapid prototyping |
| **MongoDB** | NoSQL flexibility; JSON-like document model; easy scaling |
| **React Context** | Lightweight state management; no extra dependencies |
| **Random Forest ML** | Good for mixed data types; handles non-linear relationships; fast inference |
| **FastAPI Backend** | Fast Python framework; Pydantic validation; async support |

---

## 💡 Interview Talking Points

### Problem Solved
"This e-commerce platform solves the problem of **helping construction material buyers choose the right brick type** based on their project requirements using machine learning."

### Technical Highlights

1. **Full-Stack Architecture**: 
   - Modern Next.js frontend with TypeScript
   - Node.js backend with MongoDB
   - Separate Python ML microservice

2. **ML Integration**:
   - Trained Random Forest model predicts brick recommendations
   - Handles both numeric (budget, price) and categorical (construction type) features
   - Provides confidence scores and multiple predictions

3. **State Management**:
   - React Context for auth and cart (lightweight, no Redux)
   - Per-user localStorage cart persistence
   - Automatic sync on login/logout

4. **Scalability**:
   - ML service isolated from web server
   - Can scale ML inference independently
   - API-based architecture allows easy extensions

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Type safety across frontend-backend | TypeScript throughout stack |
| ML feature preprocessing consistency | sklearn Pipeline ensures preprocessing in training & prediction match |
| Cart state across devices | localStorage + Context API |
| Mixed data types in ML | Random Forest + OneHotEncoder handles this naturally |
| ML service reliability | Next.js acts as circuit breaker with error handling |

---

## 🔍 How to Explore the Code

### Quick Tour Path

1. Start with `/components/RecommendationWidget.tsx` - See the UI form
2. Check `/app/api/recommend/route.ts` - See the API bridge
3. Review `/ml/api.py` - See FastAPI endpoint
4. Deep dive into `/ml/recommendation_pipeline.py` - Core ML logic
5. Check `/context/AuthContext.tsx` - State management pattern
6. Review `/lib/models/` - Database schema understanding

---

## 🎓 For Interview

**When asked about this project**:

> "This is a full-stack e-commerce platform for construction materials featuring an **ML-powered recommendation engine**. The system uses **Next.js** for the frontend, **MongoDB** for data persistence, and a **separate Python/FastAPI microservice** for machine learning. The recommendation system is built with **scikit-learn's Random Forest classifier** that analyzes 8 features (construction type, budget, requirements, etc.) and recommends the optimal brick grade. The ML pipeline handles mixed data types through preprocessing (OneHotEncoding for categorical, median imputation for numeric), ensuring consistent preprocessing across training and inference. The architecture is designed for scalability with the ML service isolated from the main web server."

---

**Good luck with your interview! 🚀**
