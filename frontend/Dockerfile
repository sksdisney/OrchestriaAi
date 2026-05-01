FROM node:20-alpine

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm install

# Copy the rest of the code in development only if not using a bind mount
# (docker-compose will mount the code for dev, so this is for production)
COPY . .

# Ensure node_modules is available inside the container even with bind mount
VOLUME ["/app/node_modules"]

CMD ["npm", "run", "dev"]