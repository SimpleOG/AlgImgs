import math
import wave

import numpy as np
import pydub.generators
from numpy import fft


def pitch_shift(time, modulation_speed):
    return np.sin(2 * np.pi * modulation_speed * time)


#
#
# # Преобразование mp3 в wav и вытаскивание параметов и аудио
# def ProcessSound(soundDstn: str, newDstn: str):
#     audio = pydub.generators.AudioSegment.from_mp3((soundDstn))
#     # Экспорт в WAV
#     audio.export(newDstn, format="wav")
#
#
#
#
# def change_pitch(SoundDstn, NewDstn, bucket_size=1024):  # аудио, герцы,  размер бакета со звуком
#
#     # Сохраняем аудио в правильном формате
#     ProcessSound(SoundDstn, NewDstn)
#
#     # Открываем исходный аудиофайл
#     with wave.open(NewDstn, 'rb') as wf:
#         params = wf.getparams()  # Получаем параметры аудиофайла
#         n_channels, sampwidth, framerate, n_frames = params[:4]  # Извлекаем необходимые параметры
#         audio_data = np.frombuffer(wf.readframes(n_frames), dtype=np.int16)  # Читаем аудиоданные
#
#     # Применяем преобразование Фурье к аудиоданным
#     audio_fft = fft.fft(audio_data)
#
#     # Сдвигаем частоты
#     factor = 1.5  # Увеличиваем высоту звука на 50%
#     new_fft = np.zeros_like(audio_fft)  # Создаем новый массив для преобразованных данных
#     num_bins = len(audio_fft)  # Количество бинов в аудиосигнале
#     for i in range(num_bins):
#         new_index = int(i * factor)  # Новый индекс для сдвинутой частоты
#         if new_index < num_bins:  # Проверяем, чтобы новый индекс не выходил за пределы массива
#             new_fft[new_index] = audio_fft[i]  # Применяем сдвинутую частоту
#
#     # Применяем обратное преобразование Фурье для возвращения к временной области
#     new_audio_data = fft.ifft(new_fft).real  # Применяем обратное преобразование Фурье и получаем вещественную часть
#     new_audio_data = np.int16(new_audio_data)  # Преобразуем данные к типу int16 (для сохранения в файл)
#
#     # Сохраняем новые аудиоданные в файл
#     with wave.open('pitch_shifted_audio3.wav', 'wb') as wf:
#         wf.setnchannels(n_channels)  # Устанавливаем количество каналов
#         wf.setsampwidth(sampwidth)  # Устанавливаем ширину выборки
#         wf.setframerate(framerate)  # Устанавливаем частоту дискретизации
#         wf.writeframes(new_audio_data.tobytes())  # Записываем новые аудиоданные в файл

def process_sound(input_path: str, output_path: str):
    audio = pydub.AudioSegment.from_mp3(input_path)
    audio.export(output_path, format="wav")


def change_pitch(input_path: str, output_path: str, base_factor, smoothness_coef, modulation_speed,
                 chunk_size=2048):
    # Конвертация в WAV
    temp_wav = "temp_processed.wav"
    process_sound(input_path, temp_wav)

    # Читаем WAV файл
    with wave.open(temp_wav, 'rb') as wf:
        params = wf.getparams()
        n_channels, sampwidth, framerate, n_frames = params[:4]
        audio_data = np.frombuffer(wf.readframes(n_frames), dtype=np.int16)

    # Разбиваем на фрагменты для постепенного изменения тона( чтоб легче было обрабатывать)

    num_chunks = len(audio_data) // chunk_size
    processed_audio = np.zeros_like(audio_data)

    for i in range(num_chunks):
        # берём кусок записи (кол-во чанков из параметра)
        start = i * chunk_size
        end = start + chunk_size
        chunk = audio_data[start:end]

        # Считаем на сколько сильно поменять текущий набор чанков (либо выше либо ниже в зав. от curr_fact
        # относительно времени)
        time_pos = i / num_chunks
        current_factor = base_factor + smoothness_coef * pitch_shift(time_pos, modulation_speed)
        # Сдвиг частот и пересобирание элементов чанка
        chunk_fft = fft.fft(chunk)  # получается так: получаем информацию какой звук сколько раз звучит
        # то есть индекс = частоте, значение амплитуде
        shifted_fft = np.zeros_like(chunk_fft)

        for j in range(len(chunk_fft)):
            new_index = int(j * current_factor)  # новое место для модифицированной частоты
            if 0 <= new_index < len(chunk_fft):
                # тут получается что мы ставит старый звук(например индекс j был 100)
                # на новое место (был 100, стал 150 в завис. от 93 строки) и соотв. итоговый массив имеет другое звучание
                shifted_fft[new_index] += chunk_fft[j]

        # Обратное преобразование
        # пересоберем звук после сдвига
        processed_chunk = fft.ifft(shifted_fft).real  # real,потому что для звука не нужны мнимые(скорее всего)
        # обрезаем слишком огромные значения , чтобы не произошло жутких искажений
        processed_chunk = np.clip(processed_chunk, -32768, 32767).astype(np.int16)
        # готовый звук записываем в итоговый звук
        processed_audio[start:end] = processed_chunk

    # Сохраняем результат
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(processed_audio.tobytes())
