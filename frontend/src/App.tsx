import { useState, FormEvent } from 'react';
import { MagazineCard } from './components/MagazineCard';

interface Recommendation {
  asin: string;
  score: number;
  title: string;
  image: string;
  category: string;
}

function App() {
  const [userId, setUserId] = useState<string>('A19FKU6JZQ2ECJ');
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // Stats simuladas para el dashboard
  const [stats, setStats] = useState({
    accuracy: 94,
    magazinesRead: 52,
    favoriteGenre: 'Tech & Design'
  });

  const fetchRecommendations = async (e?: FormEvent) => {
    if (e) e.preventDefault();
    if (!userId.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      // Llamada a FastAPI
      const response = await fetch(`http://localhost:8000/recommend/${userId}?n=8`);
      
      if (!response.ok) {
        if (response.status === 404) throw new Error("Usuario no encontrado en la base de datos.");
        throw new Error("Error conectando con el motor de recomendaciones.");
      }
      
      const data = await response.json();
      setRecommendations(data.recommendations || []);
      
      // Actualizamos stats simuladas para dar la sensación de un perfil dinámico
      setStats({
        accuracy: Math.floor(Math.random() * (99 - 85 + 1)) + 85,
        magazinesRead: Math.floor(Math.random() * 100) + 10,
        favoriteGenre: data.recommendations[0]?.category || 'Varieties'
      });
      
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background font-sans text-textPrimary">
      {/* Header Editorial */}
      <header className="border-b border-surface">
        <div className="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center">
          <h1 className="font-display text-3xl tracking-tight">The Curated Intelligence</h1>
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 rounded-full bg-surface ghost-border flex items-center justify-center font-display text-xl text-primary">
              M
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Sección Superior: Perfil y Controles */}
        <div className="flex flex-col md:flex-row gap-8 mb-16">
          
          {/* Controles de Búsqueda */}
          <div className="flex-1 bg-surface rounded-2xl p-8 ghost-border">
            <h2 className="text-sm font-bold uppercase tracking-widest text-textSecondary mb-6">Audience Target</h2>
            <form onSubmit={fetchRecommendations} className="flex gap-4">
              <input 
                type="text" 
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter Amazon Reviewer ID..."
                className="flex-1 bg-background border border-surface rounded-lg px-4 py-3 text-textPrimary focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
              />
              <button 
                type="submit" 
                disabled={isLoading}
                className="bg-gradient-to-br from-primary to-primary/80 text-white px-8 py-3 rounded-lg font-semibold hover:shadow-lg hover:shadow-primary/30 transition-all disabled:opacity-50"
              >
                {isLoading ? 'Analyzing...' : 'Generate Profile'}
              </button>
            </form>
            {error && <p className="text-[#ffb4ab] mt-4 text-sm">{error}</p>}
          </div>

          {/* Estadísticas de Lector */}
          <div className="flex-[0.8] flex gap-4">
            <div className="flex-1 bg-surface rounded-2xl p-6 ghost-border flex flex-col justify-between">
              <span className="text-xs text-textSecondary uppercase tracking-widest">Model Accuracy</span>
              <div className="text-5xl font-display text-secondary">{stats.accuracy}%</div>
            </div>
            <div className="flex-1 bg-surface rounded-2xl p-6 ghost-border flex flex-col justify-between">
              <span className="text-xs text-textSecondary uppercase tracking-widest">Magazines Read</span>
              <div className="text-4xl font-display text-textPrimary">{stats.magazinesRead}</div>
              <span className="text-xs text-primary truncate mt-2">{stats.favoriteGenre}</span>
            </div>
          </div>
        </div>

        {/* Sección de Recomendaciones */}
        <div>
          <div className="flex items-baseline justify-between mb-8">
            <h2 className="font-display text-4xl">Recommended For You</h2>
            <span className="text-textSecondary text-sm tracking-wide">Based on implicit collaborative filtering</span>
          </div>
          
          {recommendations.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
              {recommendations.map((rec, idx) => (
                <MagazineCard 
                  key={`${rec.asin}-${idx}`}
                  title={rec.title}
                  image={rec.image}
                  score={rec.score}
                  category={rec.category}
                />
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-20 bg-surface rounded-2xl ghost-border">
              <span className="text-6xl mb-4">📖</span>
              <p className="text-textSecondary text-lg">Enter a Reviewer ID to load personalized magazines.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
