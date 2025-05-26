# Base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency configs
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY . .

# Build production app
RUN npm run build

# Expose port used by Vite preview
EXPOSE 4173

# Start using vite preview
CMD ["npm", "run", "preview"]
