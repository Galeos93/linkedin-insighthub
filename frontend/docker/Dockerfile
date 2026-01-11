# Use official Node image
FROM node:20-slim

# Set working directory
WORKDIR /app

# Environment
ENV NODE_ENV=production
ENV PORT=3000

# Copy dependency files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build React app
RUN npm run build

# Install serve to serve the build folder
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve the build folder
CMD ["serve", "dist", "-l", "3000", "--single"]
