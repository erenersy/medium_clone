import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { postApi } from "../api/postApi";
import { tagApi } from "../api/tagApi";

export default function Sidebar({ seciliEtiketler, onEtiketSec }) {
  const [oneCikanlar, setOneCikanlar] = useState([]);
  const [etiketler, setEtiketler] = useState([]);

  useEffect(() => {
    postApi.getFeatured().then((res) => setOneCikanlar(res.data));
    tagApi.getAll().then((res) => setEtiketler(res.data));
  }, []);

  return (
    <aside className="hidden lg:block w-80 shrink-0 border-l border-voice-border pl-8 py-8">
      <h3 className="font-bold text-voice-black mb-4">Öne Çıkanlar</h3>
      {oneCikanlar.length === 0 ? (
        <p className="text-sm text-voice-gray">Henüz öne çıkan yazı yok.</p>
      ) : (
        oneCikanlar.map((yazi) => (
          <Link key={yazi.id} to={`/yazi/${yazi.id}`} className="block mb-4">
            <p className="text-xs text-voice-gray">{yazi.yazar_isim}</p>
            <p className="text-sm font-bold text-voice-black hover:underline">
              {yazi.baslik}
            </p>
          </Link>
        ))
      )}

      <h3 className="font-bold text-voice-black mt-8 mb-4">Önerilen Konular</h3>
      <div className="flex flex-wrap gap-2">
        {seciliEtiketler.length > 0 && (
          <button
            onClick={() => onEtiketSec(null)}
            className="text-sm bg-voice-black text-white rounded-full px-4 py-1.5"
          >
            Tümü ✕
          </button>
        )}
        {etiketler.map((etiket) => {
          const secili = seciliEtiketler.includes(etiket.isim);
          return (
            <button
              key={etiket.id}
              onClick={() => onEtiketSec(etiket.isim)}
              className={`text-sm rounded-full px-4 py-1.5 ${
                secili
                  ? "bg-voice-black text-white"
                  : "bg-gray-100 text-voice-black hover:bg-gray-200"
              }`}
            >
              {etiket.isim}
            </button>
          );
        })}
      </div>
    </aside>
  );
}