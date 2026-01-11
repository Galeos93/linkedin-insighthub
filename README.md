# LinkedIn Saved Jobs Insights

This project provides an end-to-end workflow to extract, upload, and analyze insights from your LinkedIn **Saved Jobs** using a locally installed browser extension and a Dockerized web application.

The system consists of three main parts:

* A **LinkedIn browser extension** to export saved jobs data
* A **backend API** for processing and analysis
* A **frontend web application** for visualization and insights

---

## Architecture Overview

```
LinkedIn Extension  →  JSON Export
                          ↓
                    Frontend (Upload)
                          ↓
                    Backend (Processing)
                          ↓
                  Insights & Visualizations
```

---

## Prerequisites

Before getting started, ensure you have the following installed:

* **Docker** and **Docker Compose**
* **Google Chrome** or any Chromium-based browser (for the extension)
* **Node.js** (only if developing the frontend locally)
* **Python 3.10+** (only if developing the backend locally)

---

## Installation & Usage

[▶ Watch the demo video](/demo.webm)

### 1. Install the LinkedIn Extension (Local)

1. Open your browser and navigate to:

   ```
   chrome://extensions
   ```
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select the `linkedin-extension/` directory from this repository.

The extension will now be available in your browser.

---

### 2. Export LinkedIn Saved Jobs

1. Navigate to LinkedIn Saved Jobs:

   ```
   https://www.linkedin.com/my-items/saved-jobs/
   ```
2. Click **"Export Saved Posts"** in the extension.
3. A `.json` file containing your saved jobs will be downloaded locally.

---

### 3. Start the Application

From the project root directory, run:

```bash
docker compose up
```

Docker will build and start the backend and frontend services.

Once running, Docker will output a local URL (typically `http://localhost:3000` or similar).

---

### 4. Upload Exported Data

1. Open the frontend URL in your browser.
2. Click **Upload**.
3. Select the downloaded LinkedIn JSON file.

The system will process the data and display insights about your saved jobs.

---

## Project Structure

```
.
├── backend/               # Backend service (Python)
│   ├── application/       # Application layer
│   ├── domain/            # Domain models and logic
│   ├── infrastructure/    # Persistence and integrations
│   ├── main.py            # Application entry point
│   ├── config.yaml        # Backend configuration
│   └── tests/             # Backend tests
│
├── frontend/              # Frontend (React + Vite + TypeScript)
│   ├── components/        # UI components
│   ├── api.ts             # API client
│   ├── App.tsx            # Main application component
│   └── vite.config.ts     # Vite configuration
│
├── linkedin-extension/    # Chrome extension
│   ├── content_script.js
│   ├── popup.js
│   └── manifest.json
│
├── docker-compose.yaml    # Service orchestration
├── LICENSE
└── README.md              # Project documentation
```

---

## Development Notes

### Backend

* Managed with **Poetry**
* API-first design
* Includes a Postman collection for testing

### Frontend

* Built with **React**, **TypeScript**, and **Vite**
* Upload-based workflow for JSON ingestion

### Extension

* Local-only installation
* No data is sent externally
* Operates exclusively on LinkedIn saved jobs pages

---

## Security & Privacy

* All data is processed **locally**.
* No LinkedIn credentials are stored.
* No external APIs are used to transmit user data.

---

## License

This project is licensed under the terms defined in the `LICENSE` file.

---

## Disclaimer

This project is not affiliated with, endorsed by, or associated with LinkedIn. Use at your own discretion and in accordance with LinkedIn’s terms of service.
