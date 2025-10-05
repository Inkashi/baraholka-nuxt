# Build Stage 1
FROM node:22-alpine AS build
WORKDIR /app

# Копируем только зависимости
COPY package.json package-lock.json* .npmrc* ./

# Устанавливаем зависимости
RUN npm ci --silent

# Копируем исходный код (без node_modules благодаря .dockerignore)
COPY . ./

# Собираем проект
RUN npm run build


# Build Stage 2
FROM node:22-alpine
WORKDIR /app

# Копируем только результат сборки
COPY --from=build /app/.output/ ./

ENV PORT=3000
ENV HOST=0.0.0.0
EXPOSE 3000

CMD ["node", "/app/server/index.mjs"]