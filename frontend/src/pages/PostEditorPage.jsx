import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { postApi } from "../api/postApi";

export default function PostEditorPage() {
  const { id } = useParams();
  const duzenlemeModu = Boolean(id);
  const [baslik, setBaslik] = useState("");
  const [icerik, setIcerik] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (duzenlemeModu) {
      postApi.getById(id).then((res) => {
        setBaslik(res.data.baslik);
        setIcerik(res.data.icerik);
      });
    }
  }, [id]);

  const handleKaydet = async (durum) => {
    if (duzenlemeModu) {
      await postApi.update(id, { baslik, icerik, durum });
      navigate(`/yazi/${id}`);
    } else {
      const res = await postApi.create(baslik, icerik);
      if (durum === "published") {
        await postApi.update(res.data.id, { durum: "published" });
      }
      navigate(`/yazi/${res.data.id}`);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-6 py-10">
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