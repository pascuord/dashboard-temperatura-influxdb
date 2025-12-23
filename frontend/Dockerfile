# Dockerfile para desarrollo de Vite/React

FROM node:20-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias
COPY package.json package-lock.json* ./

# Instalar las dependencias
RUN npm install

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto de desarrollo de Vite
EXPOSE 5173

# Comando para lanzar el servidor de desarrollo
CMD ["npm", "run", "dev", "--", "--host"]
