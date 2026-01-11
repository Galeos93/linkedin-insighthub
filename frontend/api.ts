
import { LinkedInPost, PopularAuthor, ProjectionPoint } from './types';

const BASE_URL = 'http://localhost:8000'; // Default FastAPI port

export const api = {
  getPosts: async (postIds?: string[]): Promise<LinkedInPost[]> => {
    const queryParams = postIds ? `?${postIds.map(id => `ids=${id}`).join('&')}` : '';
    const response = await fetch(`${BASE_URL}/users/me/posts${queryParams}`, {
      method: 'GET',
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to fetch posts');
    return response.json();
  },

  searchPosts: async (query: string): Promise<LinkedInPost[]> => {
    const response = await fetch(`${BASE_URL}/search?query=${encodeURIComponent(query)}`, 
    {
      method: 'GET',
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Search failed');
    // backend returns a list of post IDs for search; fetch full posts by IDs
    const ids: string[] = await response.json();
    if (!ids || ids.length === 0) return [];
    return await api.getPosts(ids);
  },

  savePosts: async (posts: LinkedInPost[]): Promise<{ status: string }> => {
    const response = await fetch(`${BASE_URL}/users/me/posts`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(posts)
    });
    if (!response.ok) throw new Error('Failed to save posts');
    return response.json();
  },

  getPopularAuthors: async (): Promise<PopularAuthor[]> => {
    const response = await fetch(`${BASE_URL}/popular_authors`,
    {
      method: 'GET',
      credentials: 'include',
    }
    );
    if (!response.ok) throw new Error('Failed to fetch popular authors');
    const body = await response.json();
    return body;
  },

  getProjection: async (): Promise<ProjectionPoint[]> => {
    const response = await fetch(`${BASE_URL}/projection`, 
    {
      method: 'GET',
      credentials: 'include',
    }
    );
    if (!response.ok) throw new Error('Failed to fetch projection');
    return response.json();
  },

  getWordCloudImage: async (): Promise<string> => {
    const response = await fetch(`${BASE_URL}/wordcloud`,
    {
      method: 'GET',
      credentials: 'include',
    }
    );
    if (!response.ok) throw new Error('Failed to fetch image');

    const blob = await response.blob();
    return URL.createObjectURL(blob); // Returns a string you can use as src=""
  }

};
