import { useRef, useState, useEffect } from "react";

const CROP_GENISLIK = 600;
const CROP_YUKSEKLIK = 300;

export default function CropModal({ dosya, onIptal, onTamam }) {
  const [resimUrl, setResimUrl] = useState(null);
  const [olcek, setOlcek] = useState(1);
  const [konum, setKonum] = useState({ x: 0, y: 0 });
  const [dogalBoyut, setDogalBoyut] = useState({ genislik: 0, yukseklik: 0 });
  const surukleniyorRef = useRef(false);
  const sonKonumRef = useRef({ x: 0, y: 0 });
  const imgRef = useRef(null);

  useEffect(() => {
    const url = URL.createObjectURL(dosya);
    setResimUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [dosya]);

  const handleImgLoad = (e) => {
    const img = e.target;
    setDogalBoyut({ genislik: img.naturalWidth, yukseklik: img.naturalHeight });
    // Başlangıçta resmi kırpma alanını kaplayacak şekilde ölçekle
    const baslangicOlcek = Math.max(
      CROP_GENISLIK / img.naturalWidth,
      CROP_YUKSEKLIK / img.naturalHeight
    );
    setOlcek(baslangicOlcek);
    setKonum({ x: 0, y: 0 });
  };

  const handleMouseDown = (e) => {
    surukleniyorRef.current = true;
    sonKonumRef.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseMove = (e) => {
    if (!surukleniyorRef.current) return;
    const dx = e.clientX - sonKonumRef.current.x;
    const dy = e.clientY - sonKonumRef.current.y;
    sonKonumRef.current = { x: e.clientX, y: e.clientY };
    setKonum((k) => ({ x: k.x + dx, y: k.y + dy }));
  };

  const handleMouseUp = () => {
    surukleniyorRef.current = false;
  };

  const handleKirp = () => {
    const img = imgRef.current;
    const canvas = document.createElement("canvas");
    canvas.width = CROP_GENISLIK;
    canvas.height = CROP_YUKSEKLIK;
    const ctx = canvas.getContext("2d");

    // Ekranda görünen resmin sol-üst köşesi konum (x,y)'de
    // ve olcek kadar büyütülmüş durumda.
    // Kırpma penceresinin (0,0)-(CROP_GENISLIK,CROP_YUKSEKLIK) alanının
    // doğal resimdeki karşılığını hesapla.
    const kaynakX = -konum.x / olcek;
    const kaynakY = -konum.y / olcek;
    const kaynakGenislik = CROP_GENISLIK / olcek;
    const kaynakYukseklik = CROP_YUKSEKLIK / olcek;

    ctx.drawImage(
      img,
      kaynakX, kaynakY, kaynakGenislik, kaynakYukseklik,
      0, 0, CROP_GENISLIK, CROP_YUKSEKLIK
    );

    canvas.toBlob(
      (blob) => {
        const kirpilmisDosya = new File([blob], dosya.name, { type: "image/jpeg" });
        onTamam(kirpilmisDosya);
      },
      "image/jpeg",
      0.9
    );
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6" style={{ width: "fit-content" }}>
        <h3 className="font-bold mb-3 text-voice-black">Kapak Resmini Kırp</h3>

        <div
          className="relative overflow-hidden border border-voice-border select-none bg-gray-100"
          style={{ width: CROP_GENISLIK, height: CROP_YUKSEKLIK, cursor: "grab" }}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
        >
          {resimUrl && (
            <img
              ref={imgRef}
              src={resimUrl}
              alt="Kırpılacak resim"
              onLoad={handleImgLoad}
              draggable={false}
              style={{
                position: "absolute",
                left: konum.x,
                top: konum.y,
                width: dogalBoyut.genislik * olcek,
                height: dogalBoyut.yukseklik * olcek,
                maxWidth: "none",
              }}
            />
          )}
        </div>

        <div className="flex items-center gap-3 mt-4">
          <span className="text-xs text-voice-gray">Yakınlaştır</span>
          <input
            type="range"
            min="0.1"
            max="3"
            step="0.01"
            value={olcek}
            onChange={(e) => setOlcek(Number(e.target.value))}
            className="flex-1"
          />
        </div>

        <div className="flex gap-3 mt-4 justify-end">
          <button
            onClick={onIptal}
            className="border border-voice-border rounded-full px-4 py-1.5 text-sm hover:border-voice-black"
          >
            İptal
          </button>
          <button
            onClick={handleKirp}
            className="bg-voice-black text-white rounded-full px-4 py-1.5 text-sm"
          >
            Kırp ve Yükle
          </button>
        </div>
      </div>
    </div>
  );
}