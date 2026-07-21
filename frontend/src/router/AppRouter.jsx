import { Routes, Route } from "react-router-dom";
import Navbar from "../components/Navbar";
import LeftMenu from "../components/LeftMenu";
import HomePage from "../pages/HomePage";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import PostDetailPage from "../pages/PostDetailPage";
import PostEditorPage from "../pages/PostEditorPage";
import MyDraftsPage from "../pages/MyDraftsPage";
import ProfilePage from "../pages/ProfilePage";

export default function AppRouter() {
  return (
    <>
      <Navbar />
      <div className="max-w-7xl mx-auto flex px-6">
        <LeftMenu />
        <div className="flex-1 min-w-0">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/yazi/yeni" element={<PostEditorPage />} />
            <Route path="/yazi/:id" element={<PostDetailPage />} />
            <Route path="/yazi/:id/duzenle" element={<PostEditorPage />} />
            <Route path="/yazilarim" element={<MyDraftsPage />} />
            <Route path="/profil/:id" element={<ProfilePage />} />
          </Routes>
        </div>
      </div>
    </>
  );
}