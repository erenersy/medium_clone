import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Icon, { IKON_YOLLARI } from "./Icon";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <nav className="border-b border-voice-border">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
        <Link to="/" className="text-2xl font-serif font-bold text-voice-black">
          Voice
        </Link>
        <div className="flex items-center gap-5">
          {user ? (
            <>
              <Link
                to="/yazi/yeni"
                className="flex items-center gap-1.5 text-sm text-voice-gray hover:text-voice-black"
              >
                <Icon yol={IKON_YOLLARI.yaz} size={18} />
                Yaz
              </Link>
              <button
                onClick={() => { logout(); navigate("/"); }}
                className="text-sm text-voice-gray hover:text-voice-black"
              >
                Çıkış
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm text-voice-gray hover:text-voice-black">
                Giriş
              </Link>
              <Link
                to="/register"
                className="text-sm bg-voice-black text-white px-4 py-1.5 rounded-full"
              >
                Kayıt Ol
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}