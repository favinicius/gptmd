/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: '#1152d4',
                'action-emerald': '#10b981',
                'background-light': '#f6f6f8',
                'neutral-dark': '#0d121b',
                'neutral-gray': '#4c669a',
                'surface-light': '#e7ebf3'
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
