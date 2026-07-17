import { Link } from "react-router-dom";

export default function PostCard({ post }) {
  return (
    <div className="py-6 border-b border-voice-border">
      <Link to={`/profil/${post.yazar_id}`} className="text-xs text-voice-gray hover:text-voice-black">
        {post.yazar_isim}
      </Link>
      <Link to={`/yazi/${post.id}`} className="block mt-1">
        <h2 className="text-xl font-serif font-bold text-voice-black mb-1">{post.baslik}</h2>
        <p className="text-voice-gray text-sm line-clamp-2">{post.icerik}</p>
        {post.durum === "draft" && (
          <span className="inline-block mt-2 text-xs text-voice-gray border border-voice-border rounded-full px-2 py-0.5">
            Taslak
          </span>
        )}
      </Link>
    </div>
  );
}