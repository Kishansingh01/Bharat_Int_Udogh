import Header from '@/components/Header';
import Footer from '@/components/Footer';
import RecommendationWidget from '@/components/RecommendationWidget';

export default function RecommendationDemoPage() {
  return (
    <>
      <Header />
      <main className="min-h-screen bg-gray-50 px-4 py-10 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-5xl">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">ML Recommendation Demo</h1>
            <p className="mt-2 text-gray-600">This page uses a trained machine learning model to suggest the most suitable brick for each customer requirement.</p>
          </div>
          <RecommendationWidget />
        </div>
      </main>
      <Footer />
    </>
  );
}
