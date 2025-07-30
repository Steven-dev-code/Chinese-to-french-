import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import easyocr
from PIL import Image, ImageTk
import numpy as np
import threading
import os
from datetime import datetime
import requests
import json

class ChineseTextTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Traducteur de Texte Chinois")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialisation des composants
        self.reader = easyocr.Reader(['ch_sim', 'en'])
        self.cap = None
        self.is_capturing = False
        self.current_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Traducteur de Texte Chinois", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame pour les contrôles
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Boutons de contrôle
        self.capture_btn = ttk.Button(control_frame, text="📷 Capturer", 
                                     command=self.toggle_capture)
        self.capture_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.load_btn = ttk.Button(control_frame, text="📁 Charger Image", 
                                  command=self.load_image)
        self.load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.translate_btn = ttk.Button(control_frame, text="🔄 Traduire", 
                                       command=self.translate_text, state='disabled')
        self.translate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(control_frame, text="🗑️ Effacer", 
                                   command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(control_frame, text="💾 Sauvegarder", 
                                  command=self.save_results)
        self.save_btn.pack(side=tk.LEFT)
        
        # Frame pour l'affichage
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Zone d'affichage de l'image
        image_frame = ttk.LabelFrame(display_frame, text="Image Capturée", padding="5")
        image_frame.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E, tk.N, tk.S))
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(0, weight=1)
        
        self.image_label = ttk.Label(image_frame, text="Aucune image", 
                                    background='white', relief='sunken')
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Zone de texte
        text_frame = ttk.LabelFrame(display_frame, text="Texte Détecté et Traduit", padding="5")
        text_frame.grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(1, weight=1)
        
        # Onglets pour le texte
        self.notebook = ttk.Notebook(text_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Onglet texte original
        original_frame = ttk.Frame(self.notebook)
        self.notebook.add(original_frame, text="Texte Original")
        original_frame.columnconfigure(0, weight=1)
        original_frame.rowconfigure(0, weight=1)
        
        self.original_text = tk.Text(original_frame, wrap=tk.WORD, font=('Arial', 12))
        original_scrollbar = ttk.Scrollbar(original_frame, orient=tk.VERTICAL, 
                                         command=self.original_text.yview)
        self.original_text.configure(yscrollcommand=original_scrollbar.set)
        self.original_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        original_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Onglet traduction
        translation_frame = ttk.Frame(self.notebook)
        self.notebook.add(translation_frame, text="Traduction")
        translation_frame.columnconfigure(0, weight=1)
        translation_frame.rowconfigure(0, weight=1)
        
        self.translation_text = tk.Text(translation_frame, wrap=tk.WORD, font=('Arial', 12))
        translation_scrollbar = ttk.Scrollbar(translation_frame, orient=tk.VERTICAL, 
                                            command=self.translation_text.yview)
        self.translation_text.configure(yscrollcommand=translation_scrollbar.set)
        self.translation_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        translation_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Barre de statut
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def toggle_capture(self):
        if not self.is_capturing:
            self.start_capture()
        else:
            self.stop_capture()
            
    def start_capture(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Erreur", "Impossible d'accéder à la caméra")
            return
            
        self.is_capturing = True
        self.capture_btn.configure(text="📸 Capturer l'Image")
        self.status_var.set("Caméra active - Cliquez pour capturer")
        
        # Démarrer la capture dans un thread séparé
        self.capture_thread = threading.Thread(target=self.capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
    def capture_loop(self):
        while self.is_capturing:
            ret, frame = self.cap.read()
            if ret:
                # Convertir BGR vers RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Redimensionner pour l'affichage
                height, width = frame_rgb.shape[:2]
                max_size = 400
                if width > max_size or height > max_size:
                    scale = max_size / max(width, height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    frame_rgb = cv2.resize(frame_rgb, (new_width, new_height))
                
                # Convertir en format PIL
                pil_image = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(pil_image)
                
                # Mettre à jour l'affichage
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo
                
                # Stocker l'image actuelle
                self.current_image = frame_rgb
                
            self.root.update_idletasks()
            
    def stop_capture(self):
        self.is_capturing = False
        if self.cap:
            self.cap.release()
        self.capture_btn.configure(text="📷 Capturer")
        self.status_var.set("Image capturée - Prêt pour la reconnaissance")
        self.translate_btn.configure(state='normal')
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            try:
                # Charger l'image
                image = cv2.imread(file_path)
                if image is None:
                    messagebox.showerror("Erreur", "Impossible de charger l'image")
                    return
                    
                # Convertir BGR vers RGB
                self.current_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Redimensionner pour l'affichage
                height, width = self.current_image.shape[:2]
                max_size = 400
                if width > max_size or height > max_size:
                    scale = max_size / max(width, height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    display_image = cv2.resize(self.current_image, (new_width, new_height))
                else:
                    display_image = self.current_image
                
                # Afficher l'image
                pil_image = Image.fromarray(display_image)
                photo = ImageTk.PhotoImage(pil_image)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo
                
                self.status_var.set("Image chargée - Prêt pour la reconnaissance")
                self.translate_btn.configure(state='normal')
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
                
    def translate_text(self):
        if self.current_image is None:
            messagebox.showwarning("Attention", "Aucune image à traiter")
            return
            
        self.status_var.set("Reconnaissance en cours...")
        self.root.update_idletasks()
        
        # Lancer la reconnaissance dans un thread séparé
        thread = threading.Thread(target=self.process_image)
        thread.daemon = True
        thread.start()
        
    def process_image(self):
        try:
            # Reconnaissance de texte
            results = self.reader.readtext(self.current_image)
            
            # Extraire le texte
            detected_text = ""
            for (bbox, text, prob) in results:
                if prob > 0.5:  # Seuil de confiance
                    detected_text += text + "\n"
            
            # Afficher le texte original
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, detected_text.strip())
            
            # Traduire le texte
            if detected_text.strip():
                try:
                    translated_text = self.translate_with_api(detected_text.strip())
                except Exception as e:
                    translated_text = f"Erreur de traduction: {str(e)}\n\nNote: Cette version utilise une API de traduction en ligne. Assurez-vous d'avoir une connexion Internet."
            else:
                translated_text = "Aucun texte détecté"
            
            # Afficher la traduction
            self.translation_text.delete(1.0, tk.END)
            self.translation_text.insert(1.0, translated_text)
            
            self.status_var.set("Reconnaissance et traduction terminées")
            
        except Exception as e:
            self.status_var.set("Erreur lors du traitement")
            messagebox.showerror("Erreur", f"Erreur lors du traitement: {str(e)}")
    
    def translate_with_api(self, text):
        """Traduction utilisant une API gratuite"""
        try:
            # Utilisation de l'API LibreTranslate (gratuite)
            url = "https://libretranslate.de/translate"
            payload = {
                "q": text,
                "source": "zh",
                "target": "fr"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result.get("translatedText", "Erreur de traduction")
            else:
                # Fallback: utiliser une autre API
                return self.translate_fallback(text)
                
        except Exception as e:
            return self.translate_fallback(text)
    
    def translate_fallback(self, text):
        """Méthode de fallback pour la traduction"""
        try:
            # Utilisation de l'API MyMemory (gratuite)
            url = f"https://api.mymemory.translated.net/get?q={text}&langpair=zh|fr"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("responseData", {}).get("translatedText", "Erreur de traduction")
            else:
                return "Erreur de connexion à l'API de traduction"
                
        except Exception as e:
            return f"Erreur de traduction: {str(e)}"
            
    def clear_all(self):
        self.original_text.delete(1.0, tk.END)
        self.translation_text.delete(1.0, tk.END)
        self.image_label.configure(image="", text="Aucune image")
        self.current_image = None
        self.translate_btn.configure(state='disabled')
        self.status_var.set("Prêt")
        
    def save_results(self):
        if not self.original_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Attention", "Aucun résultat à sauvegarder")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Sauvegarder les résultats",
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=== TRADUCTEUR DE TEXTE CHINOIS ===\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("=== TEXTE ORIGINAL ===\n")
                    f.write(self.original_text.get(1.0, tk.END))
                    f.write("\n\n=== TRADUCTION ===\n")
                    f.write(self.translation_text.get(1.0, tk.END))
                    
                messagebox.showinfo("Succès", "Résultats sauvegardés avec succès")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
                
    def on_closing(self):
        if self.cap:
            self.cap.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ChineseTextTranslator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 