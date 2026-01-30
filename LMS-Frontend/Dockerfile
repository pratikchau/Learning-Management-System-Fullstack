# Stage 1: Build Angular app
FROM node:18 as build

WORKDIR /app

# Copy package files from app folder
COPY app/package*.json ./

# Install dependencies
RUN npm install

# Copy all Angular source code
COPY app/ .

# Build the app
RUN npm run build --prod

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy build output to Nginx folder
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

