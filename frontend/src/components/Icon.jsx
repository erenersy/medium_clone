export const IKON_YOLLARI = {
  anaSayfa: "M4 11.5 12 5l8 6.5M6 10v9h5v-5h2v5h5v-9",
  yazilarim: "M6 4h9l4 4v12H6zM15 4v4h4M9 12h6M9 15h6M9 9h2",
  profil: "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM5 20c1.5-3.5 4.5-5 7-5s5.5 1.5 7 5",
  yaz: "M4 20h4l10-10-4-4L4 16v4ZM14 6l4 4",
  sil: "M4 7h16M9 7V4h6v3m-8 0 1 13a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-13M10 11v6M14 11v6",
};

export default function Icon({ yol, size = 20 }) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d={yol} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}