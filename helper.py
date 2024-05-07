# Import Library
from ultralytics import YOLO
import streamlit as st
import cv2
from pytube import YouTube
import os
from tempfile import NamedTemporaryFile
from streamlit_webrtc import (
    VideoTransformerBase,
    webrtc_streamer,
    WebRtcMode,
    VideoProcessorFactory,
)

# Local File
import settings
import turn

def load_model(model_path):
    model = YOLO(model_path)
    return model

def showDetectFrame(conf, model, st_frame, image, caption=None):
    # Predict the objects in the image using the YOLOv8 model
    res = model.predict(image, conf=conf)
    # Plot the detected objects on the video frame
    boxes = res[0].boxes
    res_plotted = res[0].plot()

    st_frame.image(
        res_plotted,
        caption=caption,
        channels="BGR",
    )
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


def play_youtube(conf, model):
    source_youtube = st.text_input("Silahkan Masukan Link YouTube")
    st.markdown(
        """
        <style>
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(5) > div > div.st-ak.st-as.st-ar.st-am.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-ij.st-b4.st-b5.st-an.st-ao.st-ap.st-aq.st-ae.st-af.st-ag.st-ef.st-ai.st-aj.st-fa.st-fb.st-fc.st-fd.st-fe.st-ik.st-il > div {
                background-color: #262730;
                border-radius: 5px;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    if st.button("Deteksi"):
        with st.spinner("Sedang Mendeteksi Objek..."):
            try:
                yt = YouTube(source_youtube)
                stream = yt.streams.filter(file_extension="mp4", res=720).first()
                vid_cap = cv2.VideoCapture(stream.url)

                st_frame = st.empty()
                while vid_cap.isOpened():
                    success, image = vid_cap.read()
                    if success:
                        showDetectFrame(
                            conf, model, st_frame, image, caption="Deteksi Video"
                        )
                    else:
                        vid_cap.release()
                        break
            except Exception as e:
                st.error("Ada Kesalahan Saat Memproses Link: " + str(e))


class VideoTransformer(VideoTransformerBase):
    def __init__(self, model, conf):
        self.model = model
        self.conf = conf

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        res = self.model.predict(img, show=False, conf=self.conf)
        res_plotted = res[0].plot()
        return res_plotted


def live(conf, model):
    webrtc_ctx = webrtc_streamer(
        key="object-detection",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={
            "iceServers": turn.get_ice_servers(),
            "iceTransportPolicy": "relay",
        },
        video_transformer_factory=lambda: VideoTransformer(model, conf),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        video_processor_factory=lambda: VideoProcessorFactory(fps=60),
    )


def process_uploaded_video(conf, model):
    uploaded_video = st.file_uploader(
        "Silahkan Upload Video", type=["mp4", "avi", "mov"]
    )

    if uploaded_video is not None:
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_video.read())
            temp_video_path = temp_file.name

        with open(temp_video_path, "rb") as video_file:
            video_bytes = video_file.read()
        if video_bytes:
            st.video(video_bytes)

        if st.button("Deteksi"):
            with st.spinner("Sedang Mendeteksi Objek..."):
                try:
                    vid_cap = cv2.VideoCapture(temp_video_path)
                    st_frame = st.empty()
                    while vid_cap.isOpened():
                        success, image = vid_cap.read()
                        if success:
                            showDetectFrame(
                                conf, model, st_frame, image, caption="Deteksi Video"
                            )
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error("Error loading video: " + str(e))


def play_stored_video(conf, model):
    source_vid = st.selectbox(
        "Silahkan Pilih Video yang Sudah Disediakan", settings.VIDEOS_DICT.keys()
    )

    with open(settings.VIDEOS_DICT.get(source_vid), "rb") as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)

    if st.button("Deteksi Video"):
        with st.spinner("Sedang Mendeteksi Objek..."):
            try:
                vid_cap = cv2.VideoCapture(str(settings.VIDEOS_DICT.get(source_vid)))
                st_frame = st.empty()
                while vid_cap.isOpened():
                    success, image = vid_cap.read()
                    if success:
                        showDetectFrame(
                            conf, model, st_frame, image, caption="Deteksi Video"
                        )
                    else:
                        vid_cap.release()
                        break
            except Exception as e:
                st.error("Ada Kesalahan Saat Proses Video: " + str(e))


def take_picture(conf, model):
    picture = st.camera_input("Silahkan Mengambil Gambar")

    if picture:
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(picture.read())
            temp_pict_path = temp_file.name

        if st.button("Deteksi Foto"):
            with st.spinner("Sedang Mendeteksi Objek..."):
                try:
                    vid_cap = cv2.VideoCapture(temp_pict_path)
                    st_frame = st.empty()
                    while vid_cap.isOpened():
                        success, image = vid_cap.read()
                        if success:
                            showDetectFrame(
                                conf, model, st_frame, image, caption="Deteksi Gambar"
                            )
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error("Error loading video: " + str(e))

def vid_help():
    html_temp_about1 = """
        <div>
            <h6 style="color: white">
                Untuk Mempermudah Penggunaan, Silahkan Menonton Tutorial Berikut 😉
            </h6>
        </div>
    """
    st.markdown(html_temp_about1, unsafe_allow_html=True)

    yt_url = "https://youtu.be/qN_ZyDgk3GU?si=QSVJw67gKpi2msyj"
    yt = YouTube(yt_url)
    st.video(yt.streams.first().url)