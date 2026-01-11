# Frontend - LinkedIn Saved Jobs Insights

This directory contains the frontend web application for uploading and visualizing LinkedIn saved jobs insights.

It is implemented using **React**, **TypeScript**, and **Vite**.

---

## Features

* Upload exported LinkedIn saved jobs JSON files
* Display insights and visualizations based on the uploaded data

---

## Tech Stack

* Node.js
* React + TypeScript
* Vite (development server and build tool)

---

## Project Structure

```
frontend/
├── components/        # React UI components
├── api.ts             # API client to backend
├── App.tsx            # Main application component
├── index.tsx          # React entry point
├── index.html         # HTML template
├── types.ts           # TypeScript type definitions
├── metadata.json      # App metadata
├── docker/            # Dockerfile for containerized builds
├── package.json       # NPM dependencies
├── package-lock.json  # Locked NPM dependencies
├── tsconfig.json      # TypeScript configuration
├── vite.config.ts     # Vite configuration
├── Makefile           # Optional commands for dev/build
└── README.md
```

---

## Local Development

### Install dependencies

```bash
npm install
```

### Start development server

```bash
npm run dev
```

* The app will start on `http://localhost:5173` (default Vite port)
* Use this server to upload LinkedIn JSON files and view insights

---

## Production Build

### Build the application

```bash
npm run build
```

* The build output will be in the `dist/` folder
* These static files can be served by any web server or containerized using Docker

### Serve with Docker (optional)

1. Build Docker image:

```bash
docker build -f docker/Dockerfile -t linkedin-frontend .
```

2. Run container:

```bash
docker run -p 3000:3000 linkedin-frontend
```

The frontend will be accessible at `http://localhost:3000`.

---

## Notes

* The frontend communicates with the backend API to process uploaded JSON files.
* Only JSON exports from LinkedIn saved jobs are supported.
* No external data is sent; all processing is done via the backend.

---

## License

See the root `LICENSE
