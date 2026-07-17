import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [eposta, setEposta] = useState("");
  const [sifre, setSifre] = useState("");
  const [hata, setHata] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setHata("");
    try {
      await login(eposta, sifre);
      navigate("/");
    } catch {
      setHata("Eposta veya şifre hatalı.");
    }
  };

  return (
    <div className="max-w-sm mx-auto px-6 py-16">
      <h1 className="text-2xl font-serif font-bold text-center mb-8">Giriş Yap</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="email" placeholder="Eposta" value={eposta}
          onChange={(e) => setEposta(e.target.value)}
          className="border border-voice-border rounded px-3 py-2"
          required
        />
        <input
          type="password" placeholder="Şifre" value={sifre}
          onChange={(e) => setSifre(e.target.value)}
          className="border border-voice-border rounded px-3 py-2"
          required
        />
        {hata && <p className="text-red-500 text-sm">{hata}</p>}
        <button type="submit" className="bg-voice-black text-white rounded-full py-2">
          Giriş Yap
        </button>
      </form>
      <p className="text-center text-sm text-voice-gray mt-4">
        Hesabın yok mu? <Link to="/register" className="underline">Kayıt ol</Link>
      </p>
    </div>
  );
}