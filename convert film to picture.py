import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tqdm import tqdm
from moviepy.editor import VideoFileClip


def remove_audio(video_path, temp_path):
    video_clip = VideoFileClip(video_path)
    video_clip_without_audio = video_clip.volumex(0)
    video_clip_without_audio.write_videofile(temp_path, codec='libx264', audio_codec='aac')
    video_clip.close()


def video_to_frames(video_path, output_dir, start_time=0, end_time=None, num_frames=60, image_format='jpg', quality=95):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        messagebox.showerror("خطا", "عدم توانایی بارگذاری ویدیو.")
        return

    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    if end_time is None or end_time > duration:
        end_time = duration

    # محاسبه فاصله فریم‌ها
    frame_interval = (end_time - start_time) / num_frames
    start_frame = int(start_time * fps)
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    extracted_frames = 0
    current_time = start_time
    with tqdm(total=num_frames, desc="ذخیره فریم‌ها") as pbar:
        while extracted_frames < num_frames:
            # محاسبه فریم فعلی
            current_frame = int(current_time * fps)
            video.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = video.read()

            if not ret:
                print(f"فریم قابل خواندن نیست در {current_frame}.")
                break

            # ذخیره فریم
            frame_name = os.path.join(output_dir, f"frame_{extracted_frames:03d}.{image_format}")
            success = cv2.imwrite(frame_name, frame,
                                   [int(cv2.IMWRITE_JPEG_QUALITY), quality] if image_format == 'jpg' else [])
            if success:
                print(f"ذخیره فریم شماره: {extracted_frames} در {frame_name}")
                extracted_frames += 1
            else:
                print(f"عدم توانایی ذخیره فریم شماره: {extracted_frames} در {frame_name}.")

            # به روزرسانی زمان برای فریم بعدی
            current_time += frame_interval

            pbar.update(1)

    video.release()
    messagebox.showinfo("موفقیت", "تمام فریم‌ها با موفقیت ذخیره شدند.")


def main():
    root = tk.Tk()
    root.withdraw()

    video_path = filedialog.askopenfilename(title="انتخاب فایل ویدیو", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if not video_path:
        return

    temp_video_path = 'temp_video.mp4'
    remove_audio(video_path, temp_video_path)

    start_time = simpledialog.askfloat("زمان شروع", "لطفاً زمان شروع (ثانیه) را وارد کنید:", minvalue=0, maxvalue=60)
    end_time = simpledialog.askfloat("زمان پایان", "لطفاً زمان پایان (ثانیه) را وارد کنید:", minvalue=start_time, maxvalue=60)

    output_directory = filedialog.askdirectory(title="انتخاب پوشه خروجی")
    if not output_directory:
        return

    image_format = simpledialog.askstring("فرمت تصویر", "لطفاً فرمت تصویر (jpg یا png) را وارد کنید:", initialvalue='jpg')
    if image_format not in ['jpg', 'png']:
        messagebox.showerror("خطا", "فرمت تصویر نامعتبر است. فقط 'jpg' و 'png' مجاز است.")
        return

    if image_format == 'jpg':
        quality = simpledialog.askinteger("کیفیت تصویر", "لطفاً کیفیت تصویر (0 تا 100) را وارد کنید:", minvalue=0,
                                          maxvalue=100, initialvalue=95)
    else:
        quality = 100

    # تعداد فریم‌ها را از کاربر بپرسید
    num_frames = simpledialog.askinteger("تعداد فریم‌ها", "لطفاً تعداد فریم‌هایی که می‌خواهید استخراج کنید را وارد کنید:", minvalue=1, maxvalue=1000)

    video_to_frames(temp_video_path, output_directory, start_time, end_time, num_frames, image_format, quality)

    os.remove(temp_video_path)


if __name__ == "__main__":
    main()
