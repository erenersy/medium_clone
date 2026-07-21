import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { postApi } from "../api/postApi";

export default function PostEditorPage() {
  const { id } = useParams();
  const duzenlemeModu = Boolean(id);
  const [baslik, setBaslik] = useState("");
  const [icerik, setIcerik] = useState("");
  const [kapakResmi, setKapakResmi] = useState(null);
  const [etiketGirdisi, setEtiketGirdisi] = useState("");
  const [etiketler, setEtiketler] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (duzenlemeModu) {
      postApi.getById(id).then((res) => {
        setBaslik(res.data.baslik);
        setIcerik(res.data.icerik);
        setKapakResmi(res.data.kapak_resmi);
        setEtiketler(res.data.etiketler);
      });
    }
  }, [id]);

  const handleResimSec = async (e) => {
    const dosya = e.target.files[0];
    if (!dosya) return;

    if (!duzenlemeModu) {
      alert("Resim eklemeden önce yazını bir kez kaydet (Taslak Kaydet).");
      return;
    }

    const res = await postApi.uploadCover(id, dosya);
    setKapakResmi(res.data.kapak_resmi);
  };

  const handleEtiketEkle = async (e) => {
    e.preventDefault();
    const temiz = etiketGirdisi.trim();
    if (!temiz) return;

    if (!duzenlemeModu) {
      alert("Etiket eklemeden önce yazını bir kez kaydet (Taslak Kaydet).");
      return;
    }

    if (etiketler.includes(temiz.toLowerCase())) {
      setEtiketGirdisi("");
      return;
    }

    await postApi.addTags(id, [temiz]);
    setEtiketler([...etiketler, temiz.toLowerCase()]);
    setEtiketGirdisi("");
  };

  const handleEtiketSil = async (etiket) => {
    await postApi.removeTag(id, etiket);
    setEtiketler(etiketler.filter((e) => e !== etiket));
  };

  const handleKaydet = async (durum) => {
    if (duzenlemeModu) {
      await postApi.update(id, { baslik, icerik, durum });
      navigate(`/yazi/${id}`);
    } else {
      const res = await postApi.create(baslik, icerik);
      navigate(`/yazi/${res.data.id}/duzenle`);
    }
  };

  const RESIM_TABANI = "http://127.0.0.1:8000";

  return (
    <div className="max-w-2xl mx-auto px-6 py-10">
      {kapakResmi && (
        <img
          src={`${RESIM_TABANI}${kapakResmi}`}
          alt="Kapak"
          className="w-full h-64 object-cover rounded mb-4"
        />
      )}

      <label className="inline-block mb-4 text-sm text-voice-gray border border-voice-border rounded-full px-4 py-2 cursor-pointer hover:border-voice-black">
        {kapakResmi ? "Kapak resmini değiştir" : "Kapak resmi ekle"}
        <input type="file" accept="image/*" onChange={handleResimSec} className="hidden" />
      </label>

      <input
        value={baslik}
        onChange={(e) => setBaslik(e.target.value)}
        placeholder="Başlık"
        className="w-full text-3xl font-serif font-bold outline-none mb-4 placeholder:text-voice-border"
      />
      <textarea
        value={icerik}
        onChange={(e) => setIcerik(e.target.value)}
        placeholder="Hikayeni anlat..."
        rows={15}
        className="w-full text-lg font-serif outline-none resize-none placeholder:text-voice-border"
      />

      <div className="mt-6 border-t border-voice-border pt-4">
        <form onSubmit={handleEtiketEkle} className="flex gap-2">
          <input
            value={etiketGirdisi}
            onChange={(e) => setEtiketGirdisi(e.target.value)}
            placeholder="Etiket ekle (ör. teknoloji)"
            className="flex-1 border border-voice-border rounded-full px-4 py-1.5 text-sm outline-none"
          />
          <button
            type="submit"
            className="border border-voice-border rounded-full px-4 py-1.5 text-sm hover:border-voice-black"
          >
            Ekle
          </button>
        </form>
        {etiketler.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-3">
            {etiketler.map((etiket) => (
              <span
                key={etiket}
                className="flex items-center gap-1.5 text-xs bg-gray-100 text-voice-black rounded-full pl-3 pr-2 py-1"
              >
                {etiket}
                <button
                  onClick={() => handleEtiketSil(etiket)}
                  className="text-voice-gray hover:text-red-500 leading-none"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="flex gap-3 mt-6 border-t border-voice-border pt-4">
        <button
          onClick={() => handleKaydet("draft")}
          className="border border-voice-border rounded-full px-5 py-2 text-sm"
        >
          Taslak Kaydet
        </button>
        <button
          onClick={() => handleKaydet("published")}
          className="bg-voice-green text-white rounded-full px-5 py-2 text-sm"
        >
          Yayınla
        </button>
      </div>
    </div>
  );
}