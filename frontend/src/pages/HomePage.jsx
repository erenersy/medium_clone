import { useEffect, useState } from "react";
import { postApi } from "../api/postApi";
import PostCard from "../components/PostCard";
import Sidebar from "../components/Sidebar";

export default function HomePage() {
  const [yazilar, setYazilar] = useState([]);
  const [seciliEtiketler, setSeciliEtiketler] = useState([]);

  const handleEtiketSec = (etiket) => {
    if (etiket === null) {
      setSeciliEtiketler([]);
      return;
    }
    setSeciliEtiketler((onceki) =>
      onceki.includes(etiket) ? onceki.filter((e) => e !== etiket) : [...onceki, etiket]
    );
  };

  useEffect(() => {
    if (seciliEtiketler.length === 0) {
      postApi.getPublished().then((res) => setYazilar(res.data));
      return;
    }
    Promise.all(seciliEtiketler.map((etiket) => postApi.getByTag(etiket))).then((sonuclar) => {
      const hepsi = sonuclar.flatMap((res) => res.data);
      const tekil = Array.from(new Map(hepsi.map((yazi) => [yazi.id, yazi])).values());
      setYazilar(tekil);
    });
  }, [seciliEtiketler]);

  return (
    <div className="max-w-6xl mx-auto px-6 flex gap-8">
      <main className="flex-1 max-w-2xl py-8">
        {seciliEtiketler.length > 0 && (
          <p className="text-sm text-voice-gray mb-4">
            <strong className="text-voice-black">{seciliEtiketler.join(", ")}</strong> etiketli yazılar
          </p>
        )}
        {yazilar.length === 0 ? (
          <p className="text-voice-gray text-center py-20">
            {seciliEtiketler.length > 0 ? "Bu etiketlerde henüz yazı yok." : "Henüz yayınlanmış yazı yok."}
          </p>
        ) : (
          yazilar.map((yazi) => <PostCard key={yazi.id} post={yazi} />)
        )}
      </main>
      <Sidebar seciliEtiketler={seciliEtiketler} onEtiketSec={handleEtiketSec} />
    </div>
  );
}