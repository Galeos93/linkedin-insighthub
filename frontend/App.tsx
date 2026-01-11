
import React, { useState, useEffect, useCallback } from 'react';
import {
  Search,
  Upload,
  BarChart2,
  Layout,
  Loader2,
  Plus,
  TrendingUp,
  Hash,
  Share2,
  FileJson
} from 'lucide-react';
import { LinkedInPost, ViewMode, PopularAuthor, ProjectionPoint } from './types';
import { api } from './api';
import PostCard from './components/PostCard';
import { PopularAuthorsChart, PostProjectionMap } from './components/Visualizations';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ViewMode>(ViewMode.FEED);
  const [posts, setPosts] = useState<LinkedInPost[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Insights State
  const [popularAuthors, setPopularAuthors] = useState<PopularAuthor[]>([]);
  const [projection, setProjection] = useState<ProjectionPoint[]>([]);
  const [wordCloudImageUrl, setWordCloudImageUrl] = useState<string | null>(null);

  const fetchPosts = async () => {
    setIsLoading(true);
    try {
      const data = await api.getPosts();
      setPosts(data);
    } catch (err) {
      console.error(err);
      // Fallback or error state
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setIsLoading(true);
    try {
      // If search query is empty, show all posts; otherwise search
      const results = searchQuery.trim() === ''
        ? await api.getPosts()
        : await api.searchPosts(searchQuery);
      setPosts(results);
      setActiveTab(ViewMode.FEED);
    } catch (err) {
      setError("Search failed. Please ensure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchInsights = async () => {
    setIsLoading(true);
    try {
      const [authors, proj, imageBlobUrl] = await Promise.all([
        api.getPopularAuthors(),
        api.getProjection(),
        api.getWordCloudImage()
      ]);
      setPopularAuthors(authors);
      setProjection(proj);
      setWordCloudImageUrl(imageBlobUrl);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch insights. Please ensure at least 10 posts are uploaded.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  useEffect(() => {
    if (activeTab === ViewMode.INSIGHTS) {
      fetchInsights();
    }
  }, [activeTab]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const content = e.target?.result as string;
        const json = JSON.parse(content);
        const postsToSave = Array.isArray(json) ? json : [json];
        await api.savePosts(postsToSave);
        await fetchPosts();
        setActiveTab(ViewMode.FEED);
      } catch (err) {
        setError("Invalid JSON format or backend error.");
      } finally {
        setIsLoading(false);
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white">
              <TrendingUp size={24} />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-700 to-indigo-700">
                InsightHub
              </h1>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">LinkedIn Analytics</p>
            </div>
          </div>

          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md mx-8 relative">
            <input
              type="text"
              placeholder="Search posts by text..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-100/50 border-none rounded-full py-2 pl-10 pr-4 text-sm focus:ring-2 focus:ring-blue-500 transition-all outline-none"
            />
            <Search className="absolute left-3 top-2.5 text-slate-400" size={18} />
          </form>

          <nav className="flex items-center gap-1">
            <NavButton
              active={activeTab === ViewMode.FEED}
              onClick={() => setActiveTab(ViewMode.FEED)}
              icon={<Layout size={20} />}
              label="Feed"
            />
            <NavButton
              active={activeTab === ViewMode.INSIGHTS}
              onClick={() => setActiveTab(ViewMode.INSIGHTS)}
              icon={<BarChart2 size={20} />}
              label="Insights"
            />
            <label className="flex items-center gap-2 px-3 py-2 text-slate-600 rounded-lg hover:bg-white hover:shadow-sm transition-all cursor-pointer">
              <Upload size={20} />
              <span className="text-sm font-medium hidden sm:inline">Upload</span>
              <input type="file" className="hidden" accept=".json" onChange={handleFileUpload} />
            </label>
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-6xl mx-auto w-full px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-red-600 animate-pulse" />
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <Loader2 className="animate-spin text-blue-600" size={40} />
            <p className="text-slate-500 animate-pulse">Syncing with LinkedIn Data...</p>
          </div>
        ) : (
          <>
            {activeTab === ViewMode.FEED && (
              <div className="space-y-6">
                <div className="flex items-center justify-between mb-2">
                  <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
                    <Hash className="text-blue-500" /> Content Discovery
                  </h2>
                  <div className="text-xs text-slate-400 font-medium">
                    Showing {posts.length} posts
                  </div>
                </div>
                {posts.length === 0 ? (
                  <div className="text-center py-20 bg-white rounded-3xl border-2 border-dashed border-slate-200">
                    <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
                      <FileJson className="text-slate-300" size={32} />
                    </div>
                    <h3 className="text-xl font-bold text-slate-700">No content found</h3>
                    <p className="text-slate-400 max-w-xs mx-auto mt-2">
                      Upload a LinkedIn posts JSON file to populate your analytics dashboard.
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {posts.map((post, idx) => (
                      <PostCard key={`${post.meta.urn}-${idx}`} post={post} />
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === ViewMode.INSIGHTS && (
              <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <PopularAuthorsChart data={popularAuthors} />

                  <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col">
                    <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                      <TrendingUp size={20} className="text-blue-500" /> Key Topics
                    </h3>
                    <div className="flex-1 flex items-center justify-center min-h-[300px] bg-slate-50 rounded-2xl overflow-hidden">
                      {wordCloudImageUrl ? (
                        <img
                          src={wordCloudImageUrl}
                          alt="Word Cloud"
                          className="max-w-full max-h-full object-contain animate-in fade-in duration-500"
                        />
                      ) : (
                        <div className="flex flex-col items-center gap-2 text-slate-400">
                          <Loader2 className="animate-spin" size={24} />
                          <p className="text-sm italic">Generating visualization...</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <PostProjectionMap data={projection} />

                {/* <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <StatCard icon={<Share2 className="text-blue-600" />} label="Avg Reach" value="2.4k" color="blue" />
                  <StatCard icon={<BarChart2 className="text-emerald-600" />} label="Post Frequency" value="12/mo" color="emerald" />
                  <StatCard icon={<TrendingUp className="text-indigo-600" />} label="Top Topic" value="MLOps" color="indigo" />
                </div> */}
              </div>
            )}
          </>
        )}
      </main>

      {/* Persistent Call-to-Action / Mobile Upload */}
      <div className="fixed bottom-6 right-6 md:hidden">
        <label className="w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg shadow-blue-200 flex items-center justify-center cursor-pointer active:scale-95 transition-transform">
          <Plus size={24} />
          <input type="file" className="hidden" accept=".json" onChange={handleFileUpload} />
        </label>
      </div>

      <footer className="py-8 border-t border-slate-100 text-center">
        <p className="text-slate-400 text-sm">© 2026 InsightHub • Designed for Data-Driven Content Strategy</p>
      </footer>
    </div>
  );
};

// UI Sub-components
const NavButton: React.FC<{ active: boolean; onClick: () => void; icon: React.ReactNode; label: string }> = ({ active, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${active
        ? 'bg-blue-50 text-blue-700 font-bold shadow-sm ring-1 ring-blue-100'
        : 'text-slate-600 hover:bg-white hover:text-slate-900'
      }`}
  >
    {icon}
    <span className="text-sm hidden sm:inline">{label}</span>
  </button>
);

const StatCard: React.FC<{ icon: React.ReactNode; label: string; value: string; color: string }> = ({ icon, label, value, color }) => (
  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
    <div className={`w-10 h-10 rounded-xl bg-${color}-50 flex items-center justify-center mb-4`}>
      {icon}
    </div>
    <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">{label}</p>
    <p className="text-2xl font-bold text-slate-800">{value}</p>
  </div>
);

export default App;
