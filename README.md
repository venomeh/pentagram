# Pentagram App

An Instagram inspired Pentagram but it uses images for socializing and user can use one's creativity for creating something unique and sharing among all!

## Prerequisites

- Node.js and npm
- Python 3.7+
- Modal.com account
- Vercel account
- Git

## Installation Steps

### 1. Frontend Setup

First, navigate to the pentagram folder and install Node.js dependencies:

```bash
cd pentagram
npm install
```

### 2. Backend Setup

Navigate to the Python folder and install the required Python packages:

```bash
cd python
pip install -r requirements.txt
```

### 3. Modal.com Setup

1. Sign up at [Modal.com](https://modal.com)
   - You'll receive $30 worth of free credits upon signup
   - These credits can be used for cloud computing resources

2. Follow Modal's deployment documentation at their official site for detailed setup instructions

### 4. Environment Configuration

Create a `.env` file in the `/pentagram` folder with the following variables:

```plaintext
# Modal credentials
API_KEY=your_modal_key  

# Vercel Blob Storage
BLOB_READ_WRITE_TOKEN=your_blob_token
```

### 5. Vercel Blob Storage Setup

1. Log in to your Vercel account
2. Set up a new Blob Storage instance
3. Generate a read/write token
4. Add the token to your `.env` file

## Usage

After completing the setup steps above, your Pentagram app will be ready to use. Access the application through the deployed URL provided by Modal.

## Support

For additional help:
- Modal Documentation: [https://modal.com/docs](https://modal.com/docs)
- Vercel Blob Storage: [https://vercel.com/docs/storage/vercel-blob](https://vercel.com/docs/storage/vercel-blob)

## Create images with your creativity!!! (more features coming soon)
