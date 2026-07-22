import { useState, useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { postApi } from "../api/postApi";
import CropModal from "../components/CropModal";
import { useEditor, EditorContent } from "@tiptap/react";
import { BubbleMenu } from "@tiptap/react/menus";
import StarterKit from "@tiptap/starter-kit";
import Link from "@tiptap/extension-link";
import Placeholder from "@tiptap/extension-placeholder";

export default function PostEditorPage() {
  const { id: urlId } = useParams();
  const [yaziId, setYaziId] = useState(urlId ? Number(urlId) : null);
  const [baslik, setBaslik] = useState("");
  const [icerik, setIcerik] = useState("");
  const [kapakResmi, setKapakResmi] = useState(null);
  const [etiketGirdisi, setEtiketGirdisi] = useState("");
  const [etiketler, setEtiketler] = useState([]);
  const [kirpilacakDosya, setKirpilacakDosya] = useState(null);
  const [kayitDurumu, setKayitDurumu] = useState("");
  const navigate = useNavigate();
  const zamanlayiciRef = useRef(null);
  const ilkYuklemeRef = useRef(true);
  const editor = useEditor({
  extensions: [
    StarterKit.configure({
      link: false,   // ← StarterKit'in kendi link eklentisini kapatıyoruz
    }),
    Link.configure({ openOnClick: false }),
    Placeholder.configure({ placeholder: "Hikayeni anlat..." }),
  ],
  content: "",
  onUpdate: ({ editor }) => {
    setIcerik(editor.getHTML());
  },
  editorProps: {
    attributes: {
      class: "prose prose-lg font-serif max-w-none outline-none min-h-[400px]",
    },
  },
});

useEffect(() => {
  if (urlId) {
    postApi.getById(urlId).then((res) => {
      setBaslik(res.data.baslik);
      setIcerik(res.data.icerik);
      setKapakResmi(res.data.kapak_resmi);
      setEtiketler(res.data.etiketler);
      if (editor && res.data.icerik) {
        editor.commands.setContent(res.data.icerik);
      }
    });
  }
}, [urlId, editor]);

  useEffect(() => {
    if (ilkYuklemeRef.current) {
      ilkYuklemeRef.current = false;
      return;
    }
    if (!baslik.trim() && !icerik.trim()) return;

    if (zamanlayiciRef.current) clearTimeout(zamanlayiciRef.current);

    zamanlayiciRef.current = setTimeout(async () => {
      setKayitDurumu("Kaydediliyor...");
      if (yaziId) {
        await postApi.update(yaziId, { baslik, icerik, durum: "draft" });
      } else {
        const res = await postApi.create(baslik || "Başlıksız Taslak", icerik);
        setYaziId(res.data.id);
        navigate(`/yazi/${res.data.id}/duzenle`, { replace: true });
      }
      setKayitDurumu("Taslak kaydedildi");
    }, 2000);

    return () => clearTimeout(zamanlayiciRef.current);
  }, [baslik, icerik]);

  const handleDosyaSecildi = (e) => {
    const dosya = e.target.files[0];
    if (!dosya) return;
    setKirpilacakDosya(dosya);
    e.target.value = "";
  };

  const handleKirpmaTamam = async (kirpilmisDosya) => {
    setKirpilacakDosya(null);

    let hedefId = yaziId;
    if (!hedefId) {
      const res = await postApi.create(baslik || "Başlıksız Taslak", icerik);
      hedefId = res.data.id;
      setYaziId(hedefId);
      navigate(`/yazi/${hedefId}/duzenle`, { replace: true });
    }

    const yuklemeRes = await postApi.uploadCover(hedefId, kirpilmisDosya);
    setKapakResmi(yuklemeRes.data.kapak_resmi);
  };

  const handleEtiketEkle = async () => {
    const temiz = etiketGirdisi.trim();
    if (!temiz || !yaziId) return;
    if (etiketler.includes(temiz.toLowerCase())) {
      setEtiketGirdisi("");
      return;
    }
    await postApi.addTags(yaziId, [temiz]);
    setEtiketler([...etiketler, temiz.toLowerCase()]);
    setEtiketGirdisi("");
  };

  const handleEtiketSil = async (etiket) => {
    await postApi.removeTag(yaziId, etiket);
    setEtiketler(etiketler.filter((e) => e !== etiket));
  };

  const handleYayinla = async () => {
    if (zamanlayiciRef.current) clearTimeout(zamanlayiciRef.current);
    let hedefId = yaziId;
    if (!hedefId) {
      const res = await postApi.create(baslik, icerik);
      hedefId = res.data.id;
    }
    await postApi.update(hedefId, { baslik, icerik, durum: "published" });
    navigate(`/yazi/${hedefId}`);
  };

  const RESIM_TABANI = "http://127.0.0.1:8000";

  return (
    <div className="max-w-2xl mx-auto px-6 py-10">
      {kirpilacakDosya && (
        <CropModal
          dosya={kirpilacakDosya}
          onIptal={() => setKirpilacakDosya(null)}
          onTamam={handleKirpmaTamam}
        />
      )}

      {kapakResmi ? (
        <>
          <img
            src={`${RESIM_TABANI}${kapakResmi}`}
            alt="Kapak"
            className="w-full h-64 object-cover rounded mb-2"
          />
          <label className="inline-block mb-4 text-xs text-voice-gray border border-voice-border rounded-full px-3 py-1.5 cursor-pointer hover:border-voice-black">
            Kapak resmini değiştir
            <input type="file" accept="image/*" onChange={handleDosyaSecildi} className="hidden" />
          </label>
        </>
      ) : (
        <label className="inline-block mb-4 text-sm text-voice-gray border border-voice-border rounded-full px-4 py-2 cursor-pointer hover:border-voice-black">
          Kapak resmi ekle
          <input type="file" accept="image/*" onChange={handleDosyaSecildi} className="hidden" />
        </label>
      )}

      <input
        value={baslik}
        onChange={(e) => setBaslik(e.target.value)}
        placeholder="Başlık"
        className="w-full text-3xl font-serif font-bold outline-none mb-4 placeholder:text-voice-border"
      />
    {editor && (
  <BubbleMenu editor={editor} className="flex items-center gap-1 bg-voice-black rounded-lg px-2 py-1.5 shadow-lg">
    <button
      onClick={() => editor.chain().focus().toggleBold().run()}
      className={`px-2 py-1 rounded text-white font-bold text-sm ${editor.isActive("bold") ? "bg-white/20" : ""}`}
    >
      B
    </button>
    <button
      onClick={() => editor.chain().focus().toggleItalic().run()}
      className={`px-2 py-1 rounded text-white italic text-sm ${editor.isActive("italic") ? "bg-white/20" : ""}`}
    >
      i
    </button>
    <button
      onClick={() => {
        const url = window.prompt("Link adresi:");
        if (url) editor.chain().focus().setLink({ href: url }).run();
      }}
      className={`px-2 py-1 rounded text-white text-sm ${editor.isActive("link") ? "bg-white/20" : ""}`}
    >
      🔗
    </button>
    <button
      onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
      className={`px-2 py-1 rounded text-white font-bold text-sm ${editor.isActive("heading", { level: 2 }) ? "bg-white/20" : ""}`}
    >
      H2
    </button>
    <button
      onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()}
      className={`px-2 py-1 rounded text-white font-semibold text-xs ${editor.isActive("heading", { level: 3 }) ? "bg-white/20" : ""}`}
    >
      H3
    </button>
    <button
      onClick={() => editor.chain().focus().toggleBlockquote().run()}
      className={`px-2 py-1 rounded text-white text-lg leading-none ${editor.isActive("blockquote") ? "bg-white/20" : ""}`}
    >
      "
    </button>
  </BubbleMenu>
)}

<EditorContent editor={editor} className="mb-6" />

      <div className="mt-6 border-t border-voice-border pt-4">
        <div className="flex gap-2">
          <input
            value={etiketGirdisi}
            onChange={(e) => setEtiketGirdisi(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleEtiketEkle()}
            placeholder="Etiket ekle (ör. teknoloji)"
            className="flex-1 border border-voice-border rounded-full px-4 py-1.5 text-sm outline-none"
          />
          <button
            type="button"
            onClick={handleEtiketEkle}
            className="border border-voice-border rounded-full px-4 py-1.5 text-sm hover:border-voice-black"
          >
            Ekle
          </button>
        </div>
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

      <div className="flex items-center gap-4 mt-6 border-t border-voice-border pt-4">
        <button
          onClick={handleYayinla}
          className="bg-voice-green text-white rounded-full px-5 py-2 text-sm"
        >
          Yayınla
        </button>
        {kayitDurumu && <span className="text-xs text-voice-gray">{kayitDurumu}</span>}
      </div>
    </div>
  );
}