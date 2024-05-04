# Import Library
import streamlit as st
from pytube import YouTube
from tempfile import NamedTemporaryFile
import base64

# Import Local File
import settings


def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            height: 100vh; /* Ukuran tinggi 100% dari viewport */
            width: 100vw; /* Ukuran lebar 100% dari viewport */
            margin: 0; /* Menghilangkan margin */
            padding: 0; /* Menghilangkan padding */
            overflow: hidden; /* Menghilangkan scroll jika konten melebihi ukuran */
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


def aboutWeb():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(" ")
    with col2:
        st.image(str(settings.IMAGE_HELP))
    with col3:
        st.write(" ")

    html_temp_about1 = """
                <div style="padding:10px; text-align:center;">
                        <h2 style="color: white">
                            DETEKSI OBJEK
                        </h2>
                    </div>
                    """
    st.markdown(html_temp_about1, unsafe_allow_html=True)

    html_temp4 = """
                <div style="padding:10px; margin-left:10%; margin-right:10%;">
                    <h4 style="text-align: justify; color: white">
                        Website ini adalah hasil dari penelitian saya tentang <strong>"Pengengalan Objek Untuk Pembelajaran Anak-Anak"</strong>.
                    </h4>
                    <h4 style="text-align: justify; color: white">
                        Website ini dibuat dengan bantuan sebuah alat bernama <a rel="noopener" href="https://streamlit.io" target="_blank">Streamlit</a>. Saya juga menggunakan teknologi <a rel="noopener" href="https://docs.ultralytics.com" target="_blank">You Only Look Once</a> (YOLO) versi 8 dari <a rel="noopener" href="https://www.ultralytics.com" target="_blank">Ultralytics</a> untuk mengembangkan modelnya.
                    </h4>
                    <h4 style="text-align: justify; color: white">
                        Dalam penelitian ini, ada 6 benda yang bisa kita kenali, yaitu: <strong>Handphone, Jam, Mobil, Orang, Sepatu,</strong> dan <strong>Tas</strong>. Website ini memiliki 4 cara untuk mengenal benda, yaitu: <strong>mengupload foto</strong>, <strong>mengupload video</strong>, <strong>menyalin link YouTube</strong>, dan <strong>deteksi langsung</strong>.
                    </h4>
                    <h4 style="text-align: justify; color: white">
                        Saya berharap website ini dapat membantu teman-teman, terutama anak-anak usia 3 - 5 tahun, untuk lebih cepat mengenal benda-benda di sekitarnya.
                    </h4>
                    <h4 style="text-align: justify; color: white">
                        Setelah mencoba website ini, tolong isi <a rel="noopener" href="https://forms.gle/k4ULtjY2ShkAegtm8" target="_blank">kuesioner</a> untuk memberikan masukan kepada saya.
                    </h4>
                    <h4 style="text-align: justify; color: white">
                        Jika ada yang ingin ditanyakan, silakan hubungi saya via <a rel="noopener" href="mailto:bie.ritan112@gmail.com">Email</a>.
                    </h4>
                    <h4 style="text-align: justify; color: white">
                        Terima kasih dan Semoga Menyenangkan!
                    </h4>
                </div>
                
                <br>
                
                <div style="padding:10px">
                    <h4 style="color: white">
                        Tambahan:
                    </h4>
                    <h4 style="color: white">
                        Mungkin pada saat mencoba mode deteksi video, youtube, dan realtime, hasilnya akan sedikit patah-patah dikarenakan proses berat yang sedang dilakukan. Mohon dimaklumi :)
                    </h4>
                </div>
                """

    st.markdown(html_temp4, unsafe_allow_html=True)
