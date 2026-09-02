import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-slate-900 text-slate-50">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400 text-center">
          Understand the Ocean. Reason Across It.
        </h1>
        <p className="text-xl text-slate-300 text-center mb-12">
          ORCA transforms heterogeneous marine observations, forecasts and scientific evidence into explainable decision intelligence.
        </p>
        <div className="flex justify-center gap-6">
          <Link href="/dashboard" className="px-8 py-4 bg-blue-600 hover:bg-blue-700 rounded-md font-semibold transition-colors shadow-lg">
            Ask ORCA
          </Link>
          <Link href="/dashboard" className="px-8 py-4 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-md font-semibold transition-colors shadow-lg">
            Explore Marine Map
          </Link>
        </div>
      </div>
    </main>
  );
}
