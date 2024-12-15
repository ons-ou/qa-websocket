# WebSocket App for Webpage Feedback

This is a FastAPI application that processes feedback from a webpage via a WebSocket endpoint.

---

## Prerequisites

Ensure you have the following installed:
- Python 3.8 or later
- `pip` (Python package manager)
- A valid `GROC_API_KEY`

---

## Getting Started

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
````

### Step 2: Add GROC_API_KEY to the .env File
`````bash
# Create a .env file in the root directory if it doesn’t exist
echo "GROC_API_KEY=<your_api_key>" > .env
`````

### Step 3: Install Dependencies
`````bash
pip install -r requirements.txt
`````
### Step 2: Add GROC_API_KEY to the .env File
`````bash
uvicorn app.main:app --reload
`````