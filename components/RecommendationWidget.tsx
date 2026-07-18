'use client';

import { useState } from 'react';

interface RecommendationFormState {
  constructionType: string;
  budget: string;
  requiredStrength: string;
  durability: string;
  brickPrice: string;
  brickQuality: string;
  customerPreference: string;
  previousOrders: string;
}

const initialState: RecommendationFormState = {
  constructionType: 'Residential',
  budget: '10000',
  requiredStrength: 'High',
  durability: 'High',
  brickPrice: '9',
  brickQuality: 'Premium',
  customerPreference: 'Durability',
  previousOrders: '0',
};

export default function RecommendationWidget() {
  const [form, setForm] = useState(initialState);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          budget: Number(form.budget),
          brickPrice: Number(form.brickPrice),
          previousOrders: Number(form.previousOrders),
        }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Unable to generate recommendation');
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  // Shared classes for larger, more spacious inputs and labels
  const labelClasses = "block text-lg font-semibold text-gray-800 mb-2";
  const inputClasses = "w-full rounded-xl border border-gray-300 bg-gray-50 px-5 py-4 text-lg text-gray-900 transition-colors focus:border-[#4a7c59] focus:bg-white focus:outline-none focus:ring-4 focus:ring-[#4a7c59]/20";

  return (
    <div className="my-10 mx-4 max-w-5xl rounded-3xl border border-gray-200 bg-white p-8 shadow-xl sm:mx-8 sm:p-12 lg:mx-auto">
      <div className="mb-10">
        <h2 className="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          Brick Recommendation
        </h2>
        <p className="mt-4  text-lg text-gray-600">
          Tell us the project context and our model will suggest the best brick type.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="grid gap-8 md:grid-cols-2">
        <div>
          <label className={labelClasses}>Construction Type</label>
          <select
            className={inputClasses}
            value={form.constructionType}
            onChange={(e) => setForm({ ...form, constructionType: e.target.value })}
          >
            <option>Residential</option>
            <option>Commercial</option>
            <option>Industrial</option>
          </select>
        </div>

        <div>
          <label className={labelClasses}>Budget</label>
          <input
            className={inputClasses}
            type="number"
            value={form.budget}
            onChange={(e) => setForm({ ...form, budget: e.target.value })}
          />
        </div>

        <div>
          <label className={labelClasses}>Required Strength</label>
          <select
            className={inputClasses}
            value={form.requiredStrength}
            onChange={(e) => setForm({ ...form, requiredStrength: e.target.value })}
          >
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
          </select>
        </div>

        <div>
          <label className={labelClasses}>Durability</label>
          <select
            className={inputClasses}
            value={form.durability}
            onChange={(e) => setForm({ ...form, durability: e.target.value })}
          >
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
          </select>
        </div>

        <div>
          <label className={labelClasses}>Brick Price</label>
          <input
            className={inputClasses}
            type="number"
            value={form.brickPrice}
            onChange={(e) => setForm({ ...form, brickPrice: e.target.value })}
          />
        </div>

        <div>
          <label className={labelClasses}>Brick Quality</label>
          <select
            className={inputClasses}
            value={form.brickQuality}
            onChange={(e) => setForm({ ...form, brickQuality: e.target.value })}
          >
            <option>Basic</option>
            <option>Standard</option>
            <option>Premium</option>
          </select>
        </div>

        <div>
          <label className={labelClasses}>Customer Preference</label>
          <select
            className={inputClasses}
            value={form.customerPreference}
            onChange={(e) => setForm({ ...form, customerPreference: e.target.value })}
          >
            <option>Budget</option>
            <option>Durability</option>
            <option>Aesthetic</option>
            <option>Cost</option>
          </select>
        </div>

        <div>
          <label className={labelClasses}>Previous Orders</label>
          <input
            className={inputClasses}
            type="number"
            value={form.previousOrders}
            onChange={(e) => setForm({ ...form, previousOrders: e.target.value })}
          />
        </div>

        <div className="mt-4 md:col-span-2">
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-2xl bg-[#4a7c59] px-6 py-5 text-xl font-bold text-white transition-transform hover:bg-[#3d6849] focus:ring-4 focus:ring-[#4a7c59]/40 active:scale-[0.99] disabled:opacity-70"
          >
            {loading ? 'Generating recommendation...' : 'Get Recommendation'}
          </button>
        </div>
      </form>

      {error && (
        <p className="mt-8 rounded-xl bg-red-50 p-6 text-lg font-medium text-red-600">
          {error}
        </p>
      )}

      {result && !loading && (
        <div className="mt-12 rounded-3xl border-2 border-emerald-200 bg-emerald-50 p-8 sm:p-10">
          <p className="text-lg font-bold uppercase tracking-wider text-emerald-700">
            Recommended Brick
          </p>
          <p className="mt-3 text-4xl font-black text-emerald-950 sm:text-5xl">
            {result.recommendedBrick}
          </p>
          <p className="mt-4 text-xl font-medium text-emerald-800">
            Confidence: {(result.confidence * 100).toFixed(1)}%
          </p>
          
          <div className="mt-8 border-t border-emerald-200/60 pt-8">
            <h4 className="mb-4 text-lg font-bold text-emerald-900">Alternative Options</h4>
            <ul className="space-y-4 text-lg text-emerald-900">
              {result.rankedOptions.map((option: any) => (
                <li key={option.brick} className="flex items-center justify-between rounded-xl bg-emerald-100/50 p-4">
                  <span className="font-semibold">{option.brick}</span>
                  <span className="font-medium">{(option.confidence * 100).toFixed(1)}%</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}