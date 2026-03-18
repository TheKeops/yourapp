<center>
  <img src="Images/yourapp_banner.png" alt="YourApp Banner">
</center>

# 🚀 YourApp | Kendi uygulamanı oluştur.
### Anlayabileceğiniz bir dil seçiniz : 

<p align="left">
  <a href="README.md"><img width="64" height="64" alt="Türkçe Dili" src="https://github.com/user-attachments/assets/dcf625d0-0bbf-41f2-bae9-eb7343c57004" /></a>
  <br>
  <a href="README_EN.md"><img width="64" height="64" alt="English Language" src="https://github.com/user-attachments/assets/671b4c55-0451-436e-bdb5-1d114029ac49" /></a>
</p>


<br>

>[!WARNING]
> Uygulama ilk sürümlerindedir. Çeşitli özellikler sınırlandırılmış veya olmayabilir, uygulamaya gelen destek ve talebe göre güncelleme atılmaktadır. Uygulama kendi deneyimlerimiz ve deneyimlerimizi geliştirmekte olduğumuz için hatalar veya anlamsız kodlar yapılar ile karşılaşabilirsiniz.

### ⚡ Temel Özellikler
- ✅ .exe formatında uygulamayı çalıştır.
- ✅ Açık kaynak proje ile kodları okuyabilirsiniz.
- ✅ Yapay zeka ile kodları yazma.
- ✅ Basit mantık ile çalışmakta.

```mermaid
graph TD
    A[Kullanıcı Seçenekleri] --->|Prompt| C(Gemini AI API)
    C -->|Kod Üretimi| D[Python Kaynak Kodu]
    D --> E{Derleme}
    E -->|PyInstaller/Compiler| F[Çalıştırılabilir Dosya .exe]
    F --> G[Kullanıcıya Teslim]
