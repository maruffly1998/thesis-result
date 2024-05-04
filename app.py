from pathlib import Path
import PIL

# Import library
import streamlit as st
import time

# Import Local File
import settings
import helper
import helperText

# Setting page layout
st.set_page_config(
    page_title="Deteksi Objek | Yolov8",
    page_icon="🔍",
)
helperText.set_background(settings.BACKGROUND)

# Load Model
confidence = settings.CONFIDENCE
model_path = Path(settings.DETECTION_MODEL)
try:
    model = helper.load_model(model_path)
except Exception as ex:
    print(f"Unable to load model. Check the specified path: {model_path}")
    print(ex)

# Main page heading
st.title("DETEKSI OBJEK 🔍")

st.markdown(
    """
	<style>
	#ffcec200 > div > span {
        color: #cdd3e9;
	}
	</style>
""",
    unsafe_allow_html=True,
)
# Pilihan deteksi
selected_option = st.selectbox("PILIH MENU:", settings.SOURCES_LIST)
st.markdown(
    """
	<style>
	.stSelectbox:first-of-type > div[data-baseweb="select"] > div {
        
        border-radius: 5px;
        
    	padding: 7px;
	}
	</style>
""",
    unsafe_allow_html=True,
)

source_img = None

# pilihan selectbox

# jika yang dipilih halaman utama
if selected_option == settings.HOME:
    helper.vid_help()

# jika yang dipilih image
elif selected_option == settings.IMAGE:
    tab1, tab2 = st.tabs(["Upload Gambar", "Ambil Gambar"])
    st.markdown(
        """
        <style>
            .stTabs [data-baseweb="tab-list"] {
                background-color: #262730;
                border-radius: 5px;
                color: #cdd3e9;
            }

            .stTabs [data-baseweb="tab"] {
                height: 50px;
                white-space: pre-wrap;
                background-color: #0000;
                border-radius: 4px 4px 0px 0px;
                gap: 1px;
                padding: 10px;
                color: #cdd3e9
            }

            .stTabs [aria-selected="true"] {
                background-color: #cdd3e9;
                color: #262730;
                font-weight: bold;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    with tab1:
        source_img = st.file_uploader(
            "Silahkan Mengupload Gambar", type=("jpg", "jpeg", "png")
        )

        col1, col2 = st.columns(2)
        res_plotted = None
        with col1:
            try:
                if source_img is None:
                    default_image_path = str(settings.DEFAULT_IMAGE)
                    default_image = PIL.Image.open(default_image_path)
                    st.image(
                        default_image_path, caption="Gambar Awal", use_column_width=True
                    )
                else:
                    uploaded_image = PIL.Image.open(source_img)
                    st.image(source_img, caption="Gambar Awal", use_column_width=True)

                    # Tombol Detect Objects di sini
                    if st.button("Deteksi", help="Klik tombol ini untuk deteksi"):
                        with col2:
                            with st.spinner("Sedang Mendeteksi Objek..."):
                                time.sleep(2)
                                res = model.predict(uploaded_image, conf=confidence)
                                boxes = res[0].boxes
                                res_plotted = res[0].plot()[:, :, ::-1]

            except Exception as ex:
                st.error("Ada Kesalahan Saat Membaca File")
                st.error(ex)

        with col2:
            if source_img is None:
                default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
                default_detected_image = PIL.Image.open(default_detected_image_path)
                st.image(
                    default_detected_image_path,
                    caption="Gambar Hasil Deteksi",
                    use_column_width=True,
                )
            else:
                if res_plotted is not None:
                    st.image(res_plotted, caption="Gambar Hasil Deteksi")
                    st.balloons()
                    class_indices = set(boxes.cls.tolist())
                    unique_labels = [settings.CLASS_NAME[idx] for idx in class_indices]

                    st.markdown(
                        """
                        <style>
                        .st-emotion-cache-13na8ym {
                            background-color: #262730;
                            color: #cdd3e9;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                    with st.expander("Hasil Deteksi"):
                        if unique_labels:
                            st.success(", ".join(unique_labels))
                        else:
                            st.warning("Tidak Ada Objek Yang Terdeteksi")
                else:
                    st.empty()
    with tab2:
        helper.take_picture(confidence, model)

# Jika pilihan video
elif selected_option == settings.VIDEO:
    tab1, tab2 = st.tabs(["Upload Video", "Sumber Asal"])
    st.markdown(
        """
        <style>
            .stTabs [data-baseweb="tab-list"] {
                background-color: #262730;
                border-radius: 5px;
                color: #cdd3e9;
            }

            .stTabs [data-baseweb="tab"] {
                height: 50px;
                white-space: pre-wrap;
                background-color: #0000;
                border-radius: 4px 4px 0px 0px;
                gap: 1px;
                padding: 10px;
                color: #cdd3e9
            }

            .stTabs [aria-selected="true"] {
                background-color: #cdd3e9;
                color: #262730;
                font-weight: bold;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    with tab1:
        helper.process_uploaded_video(confidence, model)

    with tab2:
        helper.play_stored_video(confidence, model)

# Jika pilihan youtube
elif selected_option == settings.YOUTUBE:
    helper.play_youtube(confidence, model)

# Jika pilihan realtime / webcam
elif selected_option == settings.WEBCAM:
    helper.live(confidence, model)

# Jika pilihan tentang webisite
elif selected_option == settings.ABOUT:
    helperText.aboutWeb()
