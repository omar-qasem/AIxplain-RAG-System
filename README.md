# AI-Powered RAG System with PDF Support

An intelligent Retrieval-Augmented Generation (RAG) system that allows you to upload PDF documents and ask questions about them. The system uses **aiXplain's GPT-4o Mini** to generate accurate, context-aware answers from your documents.

## 🚀 Key Features

- **📄 PDF Upload**: Upload multiple PDF documents through an intuitive web interface
- **🤖 AI-Powered Answers**: Get intelligent answers using GPT-4o Mini via aiXplain API
- **🔍 Smart Search**: TF-IDF based document retrieval with context-aware answer generation
- **💬 Natural Q&A**: Ask questions in natural language about your uploaded documents
- **📊 Document Management**: Track uploaded PDFs and indexed documents
- **🎨 Modern UI**: Beautiful, responsive interface with real-time feedback

## 🏗️ Architecture

### Backend (FastAPI + Python)
- FastAPI server with async support
- PDF text extraction using PyPDF2
- TF-IDF vectorization for document retrieval
- aiXplain API integration for answer generation
- RESTful API endpoints

### Frontend (React)
- Modern React UI with Tailwind CSS
- Drag-and-drop PDF upload
- Real-time search and results
- Responsive design

## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 16+** and **yarn**
- **aiXplain API Key** ([Get one here](https://aixplain.com))

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AIxplain-RAG-System
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
cat > .env << EOF
AIXPLAIN_API_KEY=your_actual_api_key_here
AIXPLAIN_API_URL=https://api.aixplain.com/v1
EOF

# Replace 'your_actual_api_key_here' with your actual aiXplain API key
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
yarn install

# Create .env file
cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
EOF
```

## 🚀 Running the Application

### Option 1: Using Supervisor (Production-like)

If supervisor is configured:

```bash
# Start all services
sudo supervisorctl restart all

# Check status
sudo supervisorctl status
```

### Option 2: Manual Start (Development)

**Terminal 1 - Backend:**
```bash
cd backend
python server.py
# Backend will run on http://localhost:8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
# Frontend will run on http://localhost:3000
```

## 🎯 How to Use

### 1. **Start the Application**
   - Backend: `http://localhost:8001`
   - Frontend: `http://localhost:3000`

### 2. **Upload PDF Documents**
   - Click the upload area or drag and drop PDF files
   - Wait for processing (text extraction and indexing)
   - See confirmation with page count and chunks created

### 3. **Ask Questions**
   - Type your question in the search box
   - Click "Ask AI" or press Enter
   - Get AI-generated answers with source citations

### 4. **View Results**
   - See the AI-generated answer
   - Review source documents that were used
   - Click links to view original documents (if available)

## 📚 API Endpoints

### Backend API (`http://localhost:8001`)

#### Health Check
```bash
GET /api/health
# Returns: system status, document count, PDF count, AI status
```

#### Upload PDF
```bash
POST /api/upload-pdf
Content-Type: multipart/form-data
Body: file (PDF)

# Returns: upload status, pages, chunks created
```

#### Search & Ask Question
```bash
POST /api/search
Content-Type: application/json
Body: {
  "query": "What is AI governance?",
  "top_k": 5
}

# Returns: AI answer, source documents, model used
```

#### Get Uploaded PDFs
```bash
GET /api/uploaded-pdfs
# Returns: list of uploaded PDFs with metadata
```

## 📁 Project Structure

```
AIxplain-RAG-System/
├── backend/
│   ├── server.py              # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Backend environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Tailwind styles
│   │   └── index.js          # React entry point
│   ├── package.json          # Node dependencies
│   └── .env                  # Frontend environment variables
├── guidance_ow.csv           # EPA guidance documents (default data)
├── cli_rag_agent.py          # Command-line interface (legacy)
├── rag_system.py             # Core RAG logic (legacy)
└── README.md                 # This file
```

## 🔑 Environment Variables

### Backend (.env)
```env
AIXPLAIN_API_KEY=your_aixplain_api_key
AIXPLAIN_API_URL=https://api.aixplain.com/v1
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🛠️ Configuration

### aiXplain Model
The system uses **GPT-4o Mini** (ID: `669a63646eb56306647e1091`) by default. To change the model:

1. Edit `backend/server.py`
2. Find `ModelFactory.get("669a63646eb56306647e1091")`
3. Replace with your desired model ID from aiXplain

### Document Chunking
Default settings in `server.py`:
- Chunk size: 1000 characters
- Chunk overlap: 200 characters

Adjust in the `chunk_text()` function if needed.

## 🧪 Testing

### Test Backend
```bash
# Health check
curl http://localhost:8001/api/health

# Upload PDF
curl -X POST http://localhost:8001/api/upload-pdf \
  -F "file=@/path/to/your/document.pdf"

# Search
curl -X POST http://localhost:8001/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is AI?", "top_k": 5}'
```

### Test Frontend
1. Open `http://localhost:3000` in your browser
2. Upload a test PDF
3. Ask sample questions
4. Verify AI responses and sources

## 📝 Example Queries

- "What are the main principles of AI governance?"
- "Summarize the key points about data privacy"
- "What regulations exist for autonomous vehicles?"
- "Explain the ethical considerations mentioned in the document"

## 🐛 Troubleshooting

### Backend Issues

**aiXplain API Error:**
- Verify your API key is correct in `backend/.env`
- Check API key has sufficient credits
- Ensure internet connection is stable

**PDF Upload Fails:**
- Check PDF is not corrupted
- Verify file size is reasonable (<50MB recommended)
- Ensure PyPDF2 can read the PDF format

### Frontend Issues

**Backend Connection Error:**
- Verify backend is running on port 8001
- Check `REACT_APP_BACKEND_URL` in `frontend/.env`
- Look for CORS errors in browser console

**Blank Results:**
- Check browser console for errors
- Verify backend is responding to `/api/search`
- Ensure documents are loaded (check `/api/health`)

## 📦 Dependencies

### Backend
- fastapi==0.110.1
- uvicorn==0.25.0
- aixplain==0.2.36
- PyPDF2==3.0.1
- PyMuPDF==1.26.5
- pandas==2.3.3
- scikit-learn
- python-dotenv==1.2.1

### Frontend
- react==18.2.0
- axios==1.6.8
- tailwindcss==3.4.3

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **aiXplain** for providing the AI model API
- **FastAPI** for the excellent web framework
- **React** and **Tailwind CSS** for the frontend

## 📞 Support

For issues or questions:
- Check the [Troubleshooting](#-troubleshooting) section
- Open an issue on GitHub
- Contact aiXplain support for API-related issues

