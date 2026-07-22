[33mcommit 7d1590250524e065ecd77634dfe5a56ddbe38705[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m, [m[1;31morigin/main[m[33m)[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Tue Jul 21 14:47:39 2026 +0300

    feat: otomatik kaydetme, resim kırpma, sesli okuma eklendi ve silme hataları düzeltildi
    
    - PostEditorPage'e debounce tabanlı otomatik kaydetme eklendi (2sn, useEffect+setTimeout)
    - Kapak resmi ve etiket ekleme artık taslak kaydetmeden otomatik çalışıyor
    - CropModal.jsx bileşeni eklendi: canvas tabanlı sürükle-yakınlaştır ile resim kırpma
    - CropModal'da CSS transform yerine doğal boyut/ölçek hesaplamasına geçildi (kırpma hatası düzeltildi)
    - PostDetailPage'e Web Speech API ile sesli okuma özelliği eklendi
    - Basit kelime tabanlı dil tespiti eklendi (tr-TR/en-US/de-DE), elle dil seçimi imkanı sunuldu
    - Navbar sabit yüksekliğe (h-16) alındı, LeftMenu'nün sticky top değeri buna göre hizalandı
    - Backend: yazi_sil fonksiyonu, bağlı clap ve yorum kayıtlarını silmeden yazı silme
      işleminde NOT NULL constraint hatası veriyordu; ilişkili claplar ve yorumlar artık
      yazı silinmeden önce elle temizleniyor
    - CropModal.jsx dosyasına yanlışlıkla PostDetailPage kodu yapıştırılmış olduğu tespit
      edilip düzeltildi

[33mcommit 10eabb7ace8a26de8c81a7d331ad48e2abfbd70b[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Tue Jul 21 09:55:24 2026 +0300

    feat: sol menü, ikon sistemi ve etiket yönetimi eklendi
    
    - LeftMenu bileşeni eklendi (Ana Sayfa, Yazılarım, Profilim), aktif route vurgulama
    - Ortak Icon.jsx bileşeni oluşturuldu, LeftMenu ve Navbar arasında paylaşıldı
    - Navbar sadeleştirildi, tekrar eden linkler kaldırıldı
    - PostDetailPage'de Düzenle/Sil ve yorum silme butonları pill stiline çevrildi
    - PostEditorPage'e etiket ekleme/silme arayüzü eklendi
    - Backend: PostResponse'a etiketler alanı eklendi, _post_response_olustur güncellendi
    - Backend: DELETE /yazilar/{id}/etiketler/{isim} endpoint'i eklendi
    - Backend: yaziya_etiket_ekle endpoint'i düzeltildi (response validation hatası giderildi)
    - Backend: tum_etiketleri_listele sorgusu sadece yayınlanmış yazılara bağlı etiketleri getirecek şekilde filtrelendi
    - Backend: GET /yazilar/etiket/{isim} endpoint'i eklendi (etikete göre filtreleme)
    - Sidebar'daki etiketler tıklanabilir hale getirildi, çoklu etiket seçimi (OR mantığı) eklendi

[33mcommit 4a67a24360e33265294c736bee28ff42cc68d848[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Mon Jul 20 11:33:02 2026 +0300

    feat: yazılara kapak resmi yükleme özelliği eklendi
    
    - Post modeline kapak_resmi alanı eklendi
    - PostResponse şemasına kapak_resmi dahil edildi
    - POST /yazilar/{id}/kapak-resmi endpoint'i eklendi (multipart upload)
    - Yüklenen dosyalar için uuid tabanlı isimlendirme ve uzantı kontrolü
    - main.py'de /uploads static dosya sunumu mount edildi
    - python-multipart bağımlılığı eklendi, requirements.txt oluşturuldu

[33mcommit f9f332b376138fcb97bd532c612d6bc1478cdbc2[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Fri Jul 17 14:53:05 2026 +0300

    temel frontend eklendi

[33mcommit 227a8aebcbee5f4faadf9dee6f83eb1744257df9[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Thu Jul 16 16:59:40 2026 +0300

    refactor: backend klasörleme sonrası oluşan mimari ve güvenlik hataları çözüldü

[33mcommit 48de442ac34569a29b2d298fc8c1804de46e885e[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Thu Jul 16 14:33:26 2026 +0300

    fix: taslak yazı gizlilik açıkları kapatıldı ve durum validasyonu eklendi

[33mcommit 8033a9c7b618b4696208799429c1286f4b72c918[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Thu Jul 16 13:35:57 2026 +0300

    test dosyalari silindi

[33mcommit c4d58c6ed41cc2226be39bb27b489c0c45a06a98[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Wed Jul 15 10:08:55 2026 +0300

    Endpoint'ler router'lara ayrildi, get_current_user User dondurecek sekilde guncellendi, profil endpoint'i eklendi

[33mcommit fc836dd671f217dc23875324457a8bbcd17b1356[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Tue Jul 14 09:32:47 2026 +0300

    Tum etiketleri listeleme endpoint'i eklendi

[33mcommit 1df39ff56d6e0b079a9fc1c5363b85c12745619c[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Tue Jul 14 09:31:07 2026 +0300

    Kullanici profili goruntuleme endpoint'i eklendi

[33mcommit fc2a2a71dac4f4e33f8648a0b023cf6683fd9d6a[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Tue Jul 14 09:29:20 2026 +0300

    Kullanicinin kendi yazilarini (taslak dahil) listeleme endpoint'i eklendi

[33mcommit e69090cb5941d2bf628dd6ceedeb7eae19cacb9b[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Tue Jul 14 09:23:04 2026 +0300

    Takipci ve takip edilen listeleme endpoint'leri eklendi

[33mcommit 2371c5ee3d679cd0927d5b4a4bcd115e43306fe1[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Tue Jul 14 09:11:19 2026 +0300

    refresh-token endpoint'i eklendi

[33mcommit 5653446f91873933004e46a473bb44c838f4c349[m
Author: Eren Ersoy <ereen.ersoyy@gmail.com>
Date:   Mon Jul 13 15:20:24 2026 +0300

    Medium clone: model, sema, crud ve endpoint katmanlari tamamlandi
