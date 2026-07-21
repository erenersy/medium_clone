import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { postApi } from "../api/postApi";
import { commentApi } from "../api/commentApi";
import { clapApi } from "../api/clapApi";
import { useAuth } from "../context/AuthContext";
import Icon, { IKON_YOLLARI } from "../components/Icon";

function dilTespitEt(metin) {
  const kucukMetin = metin.toLowerCase();
  const puanlar = { "tr-TR": 0, "en-US": 0, "de-DE": 0 };

  const turkceKarakterSayisi = (kucukMetin.match(/[ığşöüçİĞŞÖÜÇ]/g) || []).length;
  puanlar["tr-TR"] += turkceKarakterSayisi * 2;

  const turkceKelimeler = ["ve", "bir", "bu", "için", "değil", "ile", "çok", "ben", "sen", "de", "da"];
  const almancaKelimeler = ["der", "die", "das", "und", "ist", "nicht", "ich", "du", "mit", "ein"];
  const ingilizceKelimeler = ["the", "and", "is", "of", "to", "in", "that", "it", "you", "this"];

  kucukMetin.split(/\s+/).forEach((kelime) => {
    if (turkceKelimeler.includes(kelime)) puanlar["tr-TR"] += 1;
    if (almancaKelimeler.includes(kelime)) puanlar["de-DE"] += 1;
    if (ingilizceKelimeler.includes(kelime)) puanlar["en-US"] += 1;
  });

  return Object.entries(puanlar).sort((a, b) => b[1] - a[1])[0][0];
}

export default function PostDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [yazi, setYazi] = useState(null);
  const [yorumlar, setYorumlar] = useState([]);
  const [clapSayisi, setClapSayisi] = useState(0);
  const [yeniYorum, setYeniYorum] = useState("");
  const [hata, setHata] = useState("");
  const [okunuyor, setOkunuyor] = useState(false);
  const [secilenDil, setSecilenDil] = useState("tr-TR");

  const veriYukle = () => {
    postApi.getById(id).then((res) => setYazi(res.data)).catch(() => setHata("Yazı bulunamadı."));
    commentApi.getForPost(id).then((res) => setYorumlar(res.data));
    clapApi.getCount(id).then((res) => setClapSayisi(res.data.toplam_clap));
  };

  useEffect(() => { veriYukle(); }, [id]);

  useEffect(() => {
    if (yazi) {
      setSecilenDil(dilTespitEt(`${yazi.baslik} ${yazi.icerik}`));
    }
  }, [yazi]);

  useEffect(() => {
    return () => window.speechSynthesis.cancel();
  }, []);

  const handleClap = async () => {
    await clapApi.clap(id);
    clapApi.getCount(id).then((res) => setClapSayisi(res.data.toplam_clap));
  };

  const handleSesliOku = () => {
    if (okunuyor) {
      window.speechSynthesis.cancel();
      setOkunuyor(false);
      return;
    }
    const konusma = new SpeechSynthesisUtterance(`${yazi.baslik}. ${yazi.icerik}`);
    konusma.lang = secilenDil;

    const sesler = window.speechSynthesis.getVoices();
    const uygunSes =
      sesler.find((s) => s.lang === secilenDil) ||
      sesler.find((s) => s.lang.startsWith(secilenDil.split("-")[0]));
    if (uygunSes) konusma.voice = uygunSes;

    konusma.onend = () => setOkunuyor(false);
    window.speechSynthesis.speak(konusma);
    setOkunuyor(true);
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
        <div className="flex gap-2 mt-3">
          <Link
            to={`/yazi/${id}/duzenle`}
            className="flex items-center gap-1.5 text-xs text-voice-gray border border-voice-border rounded-full px-3 py-1.5 hover:border-voice-black hover:text-voice-black"
          >
            <Icon yol={IKON_YOLLARI.yaz} size={14} />
            Düzenle
          </Link>
          <button
            onClick={handleYaziSil}
            className="flex items-center gap-1.5 text-xs text-voice-gray border border-voice-border rounded-full px-3 py-1.5 hover:border-red-400 hover:text-red-500"
          >
            <Icon yol={IKON_YOLLARI.sil} size={14} />
            Sil
          </button>
        </div>
      )}

      <h1 className="text-3xl font-serif font-bold mt-4 mb-4">{yazi.baslik}</h1>

      <div className="flex items-center gap-3 mb-6">
        <button
          onClick={handleSesliOku}
          className="border border-voice-border rounded-full px-4 py-1.5 text-sm hover:border-voice-black"
        >
          {okunuyor ? "⏹ Durdur" : "🔊 Sesli Oku"}
        </button>
        <select
          value={secilenDil}
          onChange={(e) => setSecilenDil(e.target.value)}
          className="text-xs text-voice-gray border border-voice-border rounded-full px-2 py-1.5 outline-none"
        >
          <option value="tr-TR">Türkçe</option>
          <option value="en-US">English</option>
          <option value="de-DE">Deutsch</option>
        </select>
      </div>

      {yazi.kapak_resmi && (
        <img
          src={`http://127.0.0.1:8000${yazi.kapak_resmi}`}
          alt="Kapak"
          className="w-full rounded my-6"
        />
      )}

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
              <button
                onClick={() => handleYorumSil(yorum.id)}
                className="flex items-center gap-1 text-xs text-voice-gray border border-voice-border rounded-full px-2.5 py-1 shrink-0 ml-3 hover:border-red-400 hover:text-red-500"
              >
                <Icon yol={IKON_YOLLARI.sil} size={12} />
                Sil
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}