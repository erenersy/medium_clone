import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authApi } from "../api/authApi";
import { useAuth } from "../context/AuthContext";

export default function RegisterPage() {
  const [isim, setIsim] = useState("");
  const [eposta, setEposta] = useState("");
  const [sifre, setSifre] = useState("");
  const [hata, setHata] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setHata("");
    try {
      await authApi.register(isim, eposta, sifre);
      await login(eposta, sifre);
      navigate("/");
    } catch (err) {
      setHata(err.response?.data?.detail || "Kayıt başarısız.");
    }
  };

  return (
    <div className="max-w-sm mx-auto px-6 py-16">
      <h1 className="text-2xl font-serif font-bold text-center mb-8">Kayıt Ol</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          placeholder="İsim" value={isim}
          onChange={(e) => setIsim(e.target.value)}
          className="border border-voice-border rounded px-3 py-2" required
        />
        <input
          type="email" placeholder="Eposta" value={eposta}
          onChange={(e) => setEposta(e.target.value)}
          className="border border-voice-border rounded px-3 py-2" required
        />
        <input
          type="password" placeholder="Şifre" value={sifre}
          onChange={(e) => setSifre(e.target.value)}
          className="border border-voice-border rounded px-3 py-2" required
        />
        {hata && <p className="text-red-500 text-sm">{hata}</p>}
        <button type="submit" className="bg-voice-black text-white rounded-full py-2">
          Kayıt Ol
        </button>
      </form>
      <p className="text-center text-sm text-voice-gray mt-4">
        Zaten hesabın var mı? <Link to="/login" className="underline">Giriş yap</Link>
      </p>
    </div>
  );
}