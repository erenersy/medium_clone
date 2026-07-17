import { useEffect, useState } from "react";
import { postApi } from "../api/postApi";
import PostCard from "../components/PostCard";

export default function MyDraftsPage() {
  const [yazilar, setYazilar] = useState([]);

  useEffect(() => {
    postApi.getMine().then((res) => setYazilar(res.data));
  }, []);

  return (
    <div className="max-w-2xl mx-auto px-6 py-8">
      <h1 className="text-2xl font-serif font-bold mb-6">Yazılarım</h1>
      {yazilar.map((yazi) => <PostCard key={yazi.id} post={yazi} />)}
    </div>
  );
}