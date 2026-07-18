# E-Commerce Next.js Storefront

A modern e-commerce storefront built with Next.js, TypeScript, Tailwind CSS, and MongoDB for product browsing, cart management, authentication, and recommendation experiences.

## Features

- Responsive storefront and product catalog
- Product detail pages and cart flow
- User authentication and profile pages
- Admin order management routes
- Recommendation widget demo powered by a machine learning model
- Clean, modern UI for a construction materials brand

## Tech Stack

- Next.js
- React
- TypeScript
- Tailwind CSS
- MongoDB
- Node.js

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env.local` file and add your environment variables for MongoDB and app configuration.

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open http://localhost:3000 in your browser.

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint checks

## Project Structure

- `app/` - Pages and API routes
- `components/` - Reusable UI components
- `context/` - React context providers
- `lib/` - Database and shared logic
- `data/` - Product and testimonial data
- `ml/` - Recommendation system scripts and models

## Notes

The project includes a machine learning recommendation demo and an API route for serving recommendations. You can extend the recommendation experience by updating the model and related scripts in the `ml/` folder.
