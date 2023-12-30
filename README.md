Для запуска Flet приложений на Linux и WSL требуется установленная библиотека GStreamer. Скорее всего, у Вас уже она установлена, но если Вы получаете error while loading shared libraries: libgstapp-1.0.so.0: cannot open shared object file: No such file or directory во время работы приложения Flet, Вам нужно установить GStreamer.

Чтобы установить GStreamer на Ubuntu/Debian пропишите в терминале следующие команды:

``` bash
sudo apt-get update
sudo apt-get install -y \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
#    gstreamer1.0-doc \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio
```