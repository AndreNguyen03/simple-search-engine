# Stage 1: Build app
FROM node:20-alpine AS builder

WORKDIR /app

# Copy only dependency files first to leverage Docker cache
COPY package*.json ./
RUN npm ci

# Copy the rest of the app
COPY . .

# Build the app
RUN npm run build


# Stage 2: Run production server
FROM nginx:alpine

# Copy built app from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port (nginx serves on 80)
EXPOSE 80

# Optionally override default nginx config
# COPY nginx.conf /etc/nginx/conf.d/default.conf
