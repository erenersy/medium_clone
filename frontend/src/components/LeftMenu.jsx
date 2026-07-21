import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import Icon, { IKON_YOLLARI } from "./Icon";

export default function LeftMenu() {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) return null;

  const ogeler = [
  { etiket: "Ana Sayfa", yol: "/", ikon: IKON_YOLLARI.anaSayfa },
  { etiket: "Yazılarım", yol: "/yazilarim", ikon: IKON_YOLLARI.yazilarim },
  { etiket: "Profilim", yol: `/profil/${user.id}`, ikon: IKON_YOLLARI.profil },
];

  return (
    <nav className="hidden lg:block w-56 shrink-0 pr-8 py-8 sticky top-0 h-fit">
      {ogeler.map((oge) => {
        const aktif = oge.yol === "/" ? location.pathname === "/" : location.pathname.startsWith(oge.yol);
        return (
          <Link
            key={oge.etiket}
            to={oge.yol}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-full text-sm mb-1 ${
              aktif ? "font-semibold text-voice-black bg-gray-100" : "text-voice-gray hover:text-voice-black"
            }`}
          >
            <Icon yol={oge.ikon} />
            {oge.etiket}
          </Link>
        );
      })}
    </nav>
  );
}