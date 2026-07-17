import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { userApi } from "../api/userApi";
import { followApi } from "../api/followApi";
import { useAuth } from "../context/AuthContext";
import PostCard from "../components/PostCard";

export default function ProfilePage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [profil, setProfil] = useState(null);
  const [takipEdiyorMu, setTakipEdiyorMu] = useState(false);

  const veriYukle = () => {
    userApi.getProfile(id).then((res) => setProfil(res.data));
    if (user) {
      followApi.getFollowing(user.id).then((res) => {
        setTakipEdiyorMu(res.data.some((f) => f.takip_edilen_id === parseInt(id, 10)));
      });
    }
  };

  useEffect(() => { veriYukle(); }, [id, user]);

  const handleTakip = async () => {
    if (takipEdiyorMu) {
      await followApi.unfollow(id);
    } else {
      await followApi.follow(id);
    }
    veriYukle();
  };

  if (!profil) return <p className="text-center py-20 text-voice-gray">Yükleniyor...</p>;

  const kendiProfilim = user && user.id === profil.id;

  return (
    <div className="max-w-2xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-serif font-bold">{profil.isim}</h1>
      <p className="text-voice-gray text-sm mt-1">
        {profil.yazi_sayisi} yazı · {profil.takipci_sayisi} takipçi · {profil.takip_sayisi} takip
      </p>
      {!kendiProfilim && user && (
        <button
          onClick={handleTakip}
          className={`mt-4 rounded-full px-5 py-1.5 text-sm ${
            takipEdiyorMu ? "border border-voice-border text-voice-black" : "bg-voice-black text-white"
          }`}
        >
          {takipEdiyorMu ? "Takip Ediliyor" : "Takip Et"}
        </button>
      )}
      <div className="mt-8">
        {profil.yazilar.map((yazi) => <PostCard key={yazi.id} post={yazi} />)}
      </div>
    </div>
  );
}