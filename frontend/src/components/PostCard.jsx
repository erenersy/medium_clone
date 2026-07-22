import { Link } from "react-router-dom";

const RESIM_TABANI = "http://127.0.0.1:8000";

export default function PostCard({ post }) {

  function htmlTemizle(html) {
  const gecici = document.createElement("div");
  gecici.innerHTML = html;
  return gecici.textContent || gecici.innerText || "";
}

  return (
    <div className="py-6 border-b border-voice-border flex gap-4">
      <div className="flex-1">
        <Link to={`/profil/${post.yazar_id}`} className="text-xs text-voice-gray hover:text-voice-black">
          {post.yazar_isim}
        </Link>
        <Link to={`/yazi/${post.id}`} className="block mt-1">
          <h2 className="text-xl font-serif font-bold text-voice-black mb-1">{post.baslik}</h2>
          <p className="text-voice-gray text-sm line-clamp-2">{htmlTemizle(post.icerik)}</p>
          {post.durum === "draft" && (
            <span className="inline-block mt-2 text-xs text-voice-gray border border-voice-border rounded-full px-2 py-0.5">
              Taslak
            </span>
          )}
        </Link>
      </div>
      {post.kapak_resmi && (
        <Link to={`/yazi/${post.id}`} className="shrink-0">
          <img
            src={`${RESIM_TABANI}${post.kapak_resmi}`}
            alt=""
            className="w-28 h-28 object-cover rounded"
          />
        </Link>
      )}
    </div>
  );
}