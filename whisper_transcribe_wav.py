import whisper
import torch
import os
from pathlib import Path
import argparse

class Transcriber:
    def __init__(self, model_size="medium"):
        """
        Inicializa el modelo de transcripción
        
        Args:
            model_size: tiny, base, small, medium, large
        """
        print(f"Cargando modelo Whisper {model_size}...")
        self.model = whisper.load_model(model_size)
        self.model_size = model_size
        print("Modelo cargado exitosamente")
    
    def transcribe_audio(self, audio_path, language=None, word_timestamps=False):
        """
        Transcribe un archivo de audio
        
        Args:
            audio_path: Ruta al archivo de audio
            language: Idioma (opcional, ej: 'es', 'en')
            word_timestamps: Incluir timestamps por palabra
        """
        print(f"Transcribiendo: {audio_path}")
        
        # Opciones de transcripción
        options = {
            "language": language,
            "word_timestamps": word_timestamps,
            "fp16": torch.cuda.is_available()  # Usar GPU si disponible
        }
        
        # Filtrar opciones None
        options = {k: v for k, v in options.items() if v is not None}
        
        try:
            result = self.model.transcribe(audio_path, **options)
            return result
        except Exception as e:
            print(f"Error en transcripción: {e}")
            return None
    
    def save_transcription(self, result, output_path, format="txt"):
        """
        Guarda la transcripción en diferentes formatos
        """
        if not result:
            return False
        
        try:
            if format == "txt":
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result["text"])
            
            elif format == "srt":
                self._save_srt(result, output_path)
            
            elif format == "json":
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"Transcripción guardada: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error guardando archivo: {e}")
            return False
    
    def _save_srt(self, result, output_path):
        """Guarda en formato SRT con timestamps"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result["segments"]):
                start = self._format_timestamp(segment["start"])
                end = self._format_timestamp(segment["end"])
                
                f.write(f"{i+1}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{segment['text'].strip()}\n\n")
    
    def _format_timestamp(self, seconds):
        """Formatea segundos a timestamp HH:MM:SS,mmm"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')

def process_directory(input_dir, output_dir, model_size="medium", language=None, format="txt"):
    """
    Procesa todos los archivos de audio en un directorio
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Formatos de audio soportados
    audio_extensions = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg', '.mp4', '.avi', '.mov', '.mkv'}
    
    # Encontrar archivos de audio/video
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(input_path.glob(f"*{ext}"))
        audio_files.extend(input_path.glob(f"*{ext.upper()}"))
    
    if not audio_files:
        print("No se encontraron archivos de audio/video en el directorio")
        return
    
    print(f"Encontrados {len(audio_files)} archivos para transcribir")
    
    # Inicializar transcriber
    transcriber = Transcriber(model_size)
    
    for audio_file in audio_files:
        print(f"\n--- Procesando: {audio_file.name} ---")
        
        # Transcribir
        result = transcriber.transcribe_audio(str(audio_file), language=language)
        
        if result:
            # Crear nombre de archivo de salida
            output_file = output_path / f"{audio_file.stem}_transcription.{format}"
            
            # Guardar transcripción
            transcriber.save_transcription(result, str(output_file), format)
            
            # Mostrar estadísticas
            print(f"Duración: {result['segments'][-1]['end']:.2f}s")
            print(f"Texto: {len(result['text'])} caracteres")
        else:
            print(f"Error en la transcripción de {audio_file.name}")

def main():
    parser = argparse.ArgumentParser(description='Transcripción de audio con Whisper')
    parser.add_argument('--input', '-i', default='.', help='Directorio de entrada (default: actual)')
    parser.add_argument('--output', '-o', default='./transcripciones', help='Directorio de salida')
    parser.add_argument('--model', '-m', default='medium', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Tamaño del modelo (default: medium)')
    parser.add_argument('--language', '-l', help='Idioma (ej: es, en, fr)')
    parser.add_argument('--format', '-f', default='txt',
                       choices=['txt', 'srt', 'json'],
                       help='Formato de salida (default: txt)')
    
    args = parser.parse_args()
    
    print("=== Transcripción de Audio con Whisper ===")
    print(f"Modelo: {args.model}")
    print(f"Directorio entrada: {args.input}")
    print(f"Directorio salida: {args.output}")
    print(f"Formato: {args.format}")
    if args.language:
        print(f"Idioma: {args.language}")
    print("=" * 50)
    
    process_directory(
        input_dir=args.input,
        output_dir=args.output,
        model_size=args.model,
        language=args.language,
        format=args.format
    )

# Versión simple sin argumentos
def transcribir_carpeta_simple(carpeta_audio="./", modelo="medium", idioma="es"):
    """
    Versión simple para transcribir todos los audios de una carpeta
    """
    transcriber = Transcriber(modelo)
    
    # Buscar archivos de audio
    extensiones = ['.wav', '.mp3', '.m4a', '.mp4']
    archivos = []
    
    for ext in extensiones:
        archivos.extend(Path(carpeta_audio).glob(f"*{ext}"))
        archivos.extend(Path(carpeta_audio).glob(f"*{ext.upper()}"))
    
    for archivo in archivos:
        print(f"Transcribiendo: {archivo.name}")
        resultado = transcriber.transcribe_audio(str(archivo), language=idioma)
        
        if resultado:
            archivo_salida = Path(carpeta_audio) / f"{archivo.stem}_transcripcion.txt"
            transcriber.save_transcription(resultado, str(archivo_salida))
            print(f"✓ Completado: {archivo_salida.name}")

if __name__ == "__main__":
    # Para uso simple, descomenta la siguiente línea:
    transcribir_carpeta_simple("./wav", modelo="large", idioma="es")
    
    # Para uso con argumentos:
    # main()