
export interface LinkedInPost {
  author: string;
  profileUrl: string;
  authorImage: string;
  authorHeadline: string;
  timestamp: string;
  text: string;
  postImage?: string;
  postUrl: string;
  meta: {
    urn: string;
  };
}

export interface PopularAuthor {
  author: string;
  post_count: number;
  authorImage: string;
  authorHeadline: string;
}

export interface ProjectionPoint {
  x: number;
  y: number;
  post_id: string; // Match backend naming
  keywords: { keyword: string; score: number }[]; // Match backend structure
}

export interface WordCloudItem {
  text: string;
  size: number;
}

export enum ViewMode {
  FEED = 'FEED',
  INSIGHTS = 'INSIGHTS',
  UPLOAD = 'UPLOAD'
}
