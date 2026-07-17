import { useEffect, useState } from "react";
import { postApi } from "../api/postApi";
import PostCard from "../components/PostCard";

export default function HomePage() {
  const [yazilar, setYazilar] = useState([]);

  useEffect(() => {
    postApi.getPublished().then((res) => setYazilar(res.data));
  }, []);

  return (
    <div className="max-w-2xl mx-auto px-6 py-8">
      {yazilar.length === 0 ? (
        <p className="text-voice-gray text-center py-20">Henüz yayınlanmış yazı yok.</p>
      ) : (
        yazilar.map((yazi) => <PostCard key={yazi.id} post={yazi} />)
      )}
    </div>
  );
}