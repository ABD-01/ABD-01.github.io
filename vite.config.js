import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
    plugins: [
        tailwindcss(),
    ],
    base: './', // Ensures assets are linked relatively for GitHub Pages
    build: {
        outDir: '../dist-v5', // Output to a specific folder outside portfolio-v5 for easy deployment
        emptyOutDir: true,
    }
})
