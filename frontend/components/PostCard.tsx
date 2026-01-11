
import React, { useState } from 'react';
import { LinkedInPost } from '../types';
import { ExternalLink, User } from 'lucide-react';

interface PostCardProps {
  post: LinkedInPost;
}

const PostCard: React.FC<PostCardProps> = ({ post }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow overflow-hidden group">
      <div className="p-4">
        <div className="flex items-start justify-between mb-4">
          <div className="flex gap-3">
            <div className="relative">
              {post.authorImage ? (
                <img 
                  src={post.authorImage} 
                  alt={post.author} 
                  className="w-12 h-12 rounded-full object-cover border-2 border-slate-100"
                  onError={(e) => (e.currentTarget.src = 'https://picsum.photos/200')}
                />
              ) : (
                <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center">
                  <User className="text-slate-400" size={24} />
                </div>
              )}
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-bold text-slate-900 leading-tight group-hover:text-blue-600 transition-colors">
                <a href={post.profileUrl} target="_blank" rel="noopener noreferrer">{post.author}</a>
              </h3>
              <p className="text-xs text-slate-500 font-medium line-clamp-1">{post.authorHeadline}</p>
              <p className="text-[10px] text-slate-400 uppercase tracking-wider mt-0.5">{post.timestamp}</p>
            </div>
          </div>
          <a 
            href={post.postUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-slate-400 hover:text-blue-500 transition-colors p-1"
          >
            <ExternalLink size={18} />
          </a>
        </div>

        <div className="text-slate-700 text-sm leading-relaxed whitespace-pre-wrap break-words">
          {post.text.length > 300 ? (
            <>
              {expanded ? post.text : `${post.text.substring(0, 300)}...`}
              <button
                type="button"
                onClick={() => setExpanded(!expanded)}
                className="text-blue-600 font-semibold ml-1 hover:underline"
              >
                {expanded ? 'see less' : 'see more'}
              </button>
            </>
          ) : (
            post.text
          )}
        </div>
      </div>

      {post.postImage && (
        <div className="mt-2 border-t border-slate-50">
          <img 
            src={post.postImage} 
            alt="Post content" 
            className="w-full h-auto max-h-[500px] object-cover"
            onError={(e) => (e.currentTarget.style.display = 'none')}
          />
        </div>
      )}
      
      <div className="px-4 py-3 border-t border-slate-100 flex gap-4 text-slate-500 text-xs">
         <span className="font-medium">#{post.meta.urn.split(':').pop()}</span>
      </div>
    </div>
  );
};

export default PostCard;
