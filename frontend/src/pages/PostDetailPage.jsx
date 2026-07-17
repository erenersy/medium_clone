import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { postApi } from "../api/postApi";
import { commentApi } from "../api/commentApi";
import { clapApi } from "../api/clapApi";
import { useAuth } from "../context/AuthContext";

export default function PostDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [yazi, setYazi] = useState(null);
  const [yorumlar, setYorumlar] = useState([]);
  const [clapSayisi, setClapSayisi] = useState(0);
  const [yeniYorum, setYeniYorum] = useState("");
  const [hata, setHata] = useState("");

  const veriYukle = () => {
    postApi.getById(id).then((res) => setYazi(res.data)).catch(() => setHata("Yazı bulunamadı."));
    commentApi.getForPost(id).then((res) => setYorumlar(res.data));
    clapApi.getCount(id).then((res) => setClapSayisi(res.data.toplam_clap));
  };

  useEffect(() => { veriYukle(); }, [id]);

  const handleClap = async () => {
    await clapApi.clap(id);
    clapApi.getCount(id).then((res) => setClapSayisi(res.data.toplam_clap));
  };

  const handleYorumGonder = async (e) => {
    e.preventDefault();
    if (!yeniYorum.trim()) return;
    await commentApi.create(yeniYorum, parseInt(id, 10));
    setYeniYorum("");
    commentApi.getForPost(id).then((res) => setYorumlar(res.data));
  };

  const handleYorumSil = async (yorumId) => {
    await commentApi.remove(yorumId);
    commentApi.getForPost(id).then((res) => setYorumlar(res.data));
  };

  const handleYaziSil = async () => {
    if (!window.confirm("Bu yazıyı silmek istediğine emin misin? Bu işlem geri alınamaz.")) return;
    await postApi.remove(id);
    navigate("/");
  };

  if (hata) return <p className="text-center py-20 text-voice-gray">{hata}</p>;
  if (!yazi) return <p className="text-center py-20 text-voice-gray">Yükleniyor...</p>;

  const benimYazim = user && user.id === yazi.yazar_id;

  return (
    <div className="max-w-2xl mx-auto px-6 py-10">
      <Link to={`/profil/${yazi.yazar_id}`} className="text-sm text-voice-gray hover:text-voice-black">
        {yazi.yazar_isim}
      </Link>
      {benimYazim && (
        <div className="flex gap-3 mt-1">
          <Link to={`/yazi/${id}/duzenle`} className="text-sm text-voice-gray underline">Düzenle</Link>
          <button onClick={handleYaziSil} className="text-sm text-red-500 underline">Sil</button>
        </div>
      )}
      <h1 className="text-3xl font-serif font-bold mt-2 mb-4">{yazi.baslik}</h1>
      <p className="text-lg font-serif leading-relaxed whitespace-pre-wrap">{yazi.icerik}</p>

      <div className="flex items-center gap-3 my-8 border-y border-voice-border py-4">
        <button
          onClick={handleClap} disabled={!user}
          className="border border-voice-border rounded-full px-4 py-1.5 text-sm hover:border-voice-black disabled:opacity-40"
        >
          👏 {clapSayisi}
        </button>
      </div>

      <h3 className="font-bold mb-3">Yorumlar</h3>
      {user && (
        <form onSubmit={handleYorumGonder} className="flex gap-2 mb-6">
          <input
            value={yeniYorum} onChange={(e) => setYeniYorum(e.target.value)}
            placeholder="Yorum yaz..." className="flex-1 border border-voice-border rounded px-3 py-2 text-sm"
          />
          <button type="submit" className="bg-voice-black text-white rounded-full px-4 text-sm">Gönder</button>
        </form>
      )}
      {yorumlar.map((yorum) => (
        <div key={yorum.id} className="py-3 border-b border-voice-border text-sm">
          <div className="flex justify-between items-start">
            <div>
              <span className="font-medium text-voice-black">{yorum.yazan_isim}</span>
              <p className="text-voice-gray mt-0.5">{yorum.icerik}</p>
            </div>
            {user && user.id === yorum.yazan_id && (
              <button onClick={() => handleYorumSil(yorum.id)} className="text-xs text-red-400 underline shrink-0 ml-3">
                Sil
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}